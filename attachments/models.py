import tempfile
from pathlib import Path

from django.core.files import File
from django.db import models
from PIL import Image


class Attachment(models.Model):
    description = models.CharField(max_length=500)
    original_file = models.FileField()
    processed_file = models.FileField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.processed_file:
            return super().save(*args, **kwargs)

        try:
            image = Image.open(self.original_file.path)
        except IOError:
            return self.save(*args, **kwargs)
        max_width = 640
        if image.width > max_width:
            ratio = image.height / image.width
            height = round(max_width * ratio)
            output = image.resize((max_width, height))
        else:
            output = image.copy()
        current_path = Path(image.filename)
        temp_dir = Path(tempfile.mkdtemp())
        temp_path = temp_dir / (current_path.stem + "-resized" + current_path.suffix)
        output.save(temp_path)
        with open(temp_path, "rb") as output_file:
            f = File(output_file)
            self.processed_file.save(temp_path.name, f, save=False)
        temp_path.unlink()
        temp_dir.rmdir()
        return super().save(*args, **kwargs)
