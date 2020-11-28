from django.contrib import admin, messages
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
        "open_graph_image",
    ]
    list_display_links = ["description"]
    fields = [
        "description",
        "original_file",
        "original_file_url",
        "processed_file",
        "processed_file_url",
        "open_graph_image",
    ]
    readonly_fields = [
        "original_file_url",
        "processed_file_url",
        "open_graph_image",
    ]
    actions = ["set_as_open_graph_image"]

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

    def set_as_open_graph_image(self, request, queryset):
        if len(queryset) != 1:
            messages.error(request, "You must select only one attachment")
            return
        Attachment.objects.update(open_graph_image=False)
        queryset.update(open_graph_image=True)
        messages.success(request, "Done")

    set_as_open_graph_image.short_description = "Set as open graph image"
