from django.contrib import admin, messages
from django.contrib.admin import register
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
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
    actions = [
        "set_as_open_graph_image",
        "reprocess_selected_attachments",
    ]
    search_fields = ["description", "original_file", "processed_file"]

    class Media:
        js = ["attachments/js/copy_url.js"]

    def processed_file_url(self, instance: Attachment) -> str:
        if instance.processed_file:
            return format_html(
                '{0} <a class="copy-button" data-to-copy="{1}" href="#">&#128203;</a>',
                instance.processed_file.url,
                instance.processed_file.url,
            )
        return ""

    def original_file_url(self, instance: Attachment) -> str:
        if instance.original_file:
            return format_html(
                '{0} <a class="copy-button" data-to-copy="{1}" href="#">&#128203;</a>',
                instance.original_file.url,
                instance.original_file.url,
            )
        return ""

    @admin.action(description="Set as open graph image")
    def set_as_open_graph_image(self, request: WSGIRequest, queryset: QuerySet) -> None:
        if len(queryset) != 1:
            messages.error(request, "You must select only one attachment")
            return
        Attachment.objects.update(open_graph_image=False)
        queryset.update(open_graph_image=True)
        messages.success(request, "Done")

    @admin.action(description="Reprocess selected attachments")
    def reprocess_selected_attachments(
        self, request: WSGIRequest, queryset: QuerySet
    ) -> None:
        if len(queryset) == 0:
            messages.error(request, "You must select at least one attachment")
            return
        for attachment in queryset:
            attachment.reprocess()
        messages.success(request, "Attachments were successfully reprocessed.")
