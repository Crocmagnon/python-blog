from django.contrib import admin
from django.contrib.admin import register

from attachments.models import Attachment


@register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "original_file",
        "original_file_url",
        "processed_file",
        "processed_file_url",
    ]
    list_display_links = ["description"]

    class Media:
        js = ["attachments/js/copy_url.js"]

    def processed_file_url(self, instance):
        return instance.processed_file.url

    def original_file_url(self, instance):
        return instance.original_file.url
