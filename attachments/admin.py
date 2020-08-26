from django.contrib import admin
from django.contrib.admin import register

from attachments.models import Attachment


@register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["description", "original_file", "processed_file"]
    list_display_links = ["description"]
