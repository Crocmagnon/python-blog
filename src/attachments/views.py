from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from attachments.models import Attachment


def get_original(_request: WSGIRequest, pk: int) -> HttpResponse:
    attachment = get_object_or_404(Attachment, pk=pk)
    return HttpResponseRedirect(attachment.original_file.url)


def get_processed(_request: WSGIRequest, pk: int) -> HttpResponse:
    attachment = get_object_or_404(Attachment, pk=pk)
    return HttpResponseRedirect(attachment.processed_file.url)
