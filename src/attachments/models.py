from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path
from typing import Any

import requests
from django.conf import settings
from django.core.files import File
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.db.models.fields.files import FieldFile
from django.urls import reverse
from PIL import Image

from articles.utils import build_full_absolute_url

logger = logging.getLogger(__name__)


class AbsoluteUrlFieldFile(FieldFile):
    def get_full_absolute_url(self, request: WSGIRequest) -> str:
        return build_full_absolute_url(request, self.url)


class AbsoluteUrlFileField(models.FileField):
    attr_class = AbsoluteUrlFieldFile


class AttachmentManager(models.Manager):
    def get_open_graph_image(self) -> Attachment | None:
        return self.filter(open_graph_image=True).first()


class Attachment(models.Model):
    description = models.CharField(max_length=500)
    original_file = AbsoluteUrlFileField()
    processed_file = AbsoluteUrlFileField(blank=True, null=True)
    open_graph_image = models.BooleanField(blank=True, default=False)

    objects = AttachmentManager()

    class Meta:
        ordering = ["description"]

    def __str__(self) -> str:
        return f"{self.description} ({self.original_file.name})"

    def reprocess(self) -> None:
        self.processed_file = None  # type: ignore[assignment]
        self.save()

    @property
    def original_file_url(self) -> str:
        return reverse("attachments:original", kwargs={"pk": self.pk})

    @property
    def processed_file_url(self) -> str | None:
        if self.processed_file:
            return reverse("attachments:processed", kwargs={"pk": self.pk})
        return None

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)

        if self.processed_file:
            return None

        try:
            Image.open(self.original_file.path)
        except OSError:
            return None

        # Submit job to shortpixel
        base_data = {
            "key": settings.SHORTPIXEL_API_KEY,
            "plugin_version": "gabno",
            "wait": 20,
        }
        post_data = {
            "lossy": 1,
            "resize": 3,
            "resize_width": settings.SHORTPIXEL_RESIZE_WIDTH,
            "resize_height": settings.SHORTPIXEL_RESIZE_HEIGHT,
            "keep_exif": 1,
            "file_paths": json.dumps(
                {"img": self.original_file.path},
            ),
        }
        data = {**base_data, **post_data}
        url = "https://api.shortpixel.com/v2/post-reducer.php"
        with Path(self.original_file.path).open("rb") as original_file:
            response = requests.post(
                url=url,
                data=data,
                files={"img": original_file},
                timeout=10,
            )

        res = response.json()
        if len(res) == 0 or not isinstance(res, list):
            logger.error("Shortpixel response is not a non-empty list: %s", res)
            logger.error("POST data: %s", data)
            return super().save(*args, **kwargs)

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
            response = requests.post(url=url, data=check_data, timeout=10)
            res_data = response.json()[0]

        # Download image
        current_path = Path(self.original_file.path)
        temp_dir = Path(tempfile.mkdtemp())
        temp_path = temp_dir / (current_path.stem + "-processed" + current_path.suffix)
        img = requests.get(res_data["LossyURL"], stream=True, timeout=10)
        with Path(temp_path).open("wb") as temp_file:
            for chunk in img:
                temp_file.write(chunk)

        # Link it to our model
        with Path(temp_path).open("rb") as output_file:
            f = File(output_file)
            self.processed_file.save(temp_path.name, f, save=False)

        temp_path.unlink()
        temp_dir.rmdir()
        return super().save(*args, **kwargs)
