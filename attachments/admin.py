from django.contrib import admin
from django.contrib.admin import register
from django.utils.html import format_html

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
    fields = [
        "description",
        "original_file",
        "original_file_url",
        "processed_file",
        "processed_file_url",
    ]
    readonly_fields = [
        "original_file_url",
        "processed_file_url",
    ]

    class Media:
        js = ["attachments/js/copy_url.js"]

    def processed_file_url(self, instance):
        if instance.processed_file:
            return format_html(
                '{} <a class="copy-button" data-to-copy="{}" href="#">&#128203;</a>',
                instance.processed_file.url,
                instance.processed_file.url,
            )
        return ""

    def original_file_url(self, instance):
        if instance.original_file:
            return format_html(
                '{} <a class="copy-button" data-to-copy="{}" href="#">&#128203;</a>',
                instance.original_file.url,
                instance.original_file.url,
            )
        return ""
