import json
import tempfile
from pathlib import Path

import requests
from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models.fields.files import FieldFile
from PIL import Image

from articles.utils import build_full_absolute_url


class AbsoluteUrlFieldFile(FieldFile):
    def get_full_absolute_url(self, request):
        return build_full_absolute_url(request, self.url)


class AbsoluteUrlFileField(models.FileField):
    attr_class = AbsoluteUrlFieldFile


class AttachmentManager(models.Manager):
    def get_open_graph_image(self):
        return self.filter(open_graph_image=True).first()


class Attachment(models.Model):
    description = models.CharField(max_length=500)
    original_file = AbsoluteUrlFileField()
    processed_file = AbsoluteUrlFileField(blank=True, null=True)
    open_graph_image = models.BooleanField(blank=True)

    objects = AttachmentManager()

    class Meta:
        ordering = ["description"]

    def __str__(self):
        return f"{self.description} ({self.original_file.name})"

    def save(self, *args, **kwargs):
        if self.processed_file:
            return super().save(*args, **kwargs)

        if self.id is None:
            super().save(*args, **kwargs)
        try:
            image = Image.open(self.original_file.path)
        except IOError:
            return super().save(*args, **kwargs)

        # Submit job to shortpixel
        base_data = {
            "key": settings.SHORTPIXEL_API_KEY,
            "plugin_version": "gabno",
            "wait": 20,
        }
        post_data = {
            "lossy": 1,
            "resize": 3,
            "resize_width": 640,
            "resize_height": 10000,
            "keep_exif": 1,
            "file_paths": json.dumps(
                [f"{self.original_file.name}:{self.original_file.path}"]
            ),
        }
        data = {**base_data, **post_data}
        url = "https://api.shortpixel.com/v2/post-reducer.php"
        with open(self.original_file.path, "rb") as original_file:
            response = requests.post(
                url=url, data=data, files={self.original_file.name: original_file}
            )
        res = response.json()
        res_data = res[0]

        # Loop until it's done
        post_data = {
            "key": settings.SHORTPIXEL_API_KEY,
            "plugin_version": "gabno",
            "wait": 20,
            "file_urls": json.dumps([res_data["OriginalURL"]]),
        }
        check_data = {**base_data, **post_data}
        while res_data["Status"]["Code"] == "1":
            response = requests.post(url=url, data=check_data)
            res_data = response.json()[0]

        # Download image
        current_path = Path(self.original_file.path)
        temp_dir = Path(tempfile.mkdtemp())
        temp_path = temp_dir / (current_path.stem + "-processed" + current_path.suffix)
        img = requests.get(res_data["LossyURL"], stream=True)
        with open(temp_path, "wb") as temp_file:
            for chunk in img:
                temp_file.write(chunk)

        # Link it to our model
        with open(temp_path, "rb") as output_file:
            f = File(output_file)
            self.processed_file.save(temp_path.name, f, save=False)

        temp_path.unlink()
        temp_dir.rmdir()
        return super().save(*args, **kwargs)
