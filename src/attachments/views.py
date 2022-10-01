import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import last_modified

from attachments.models import Attachment


def get_updated_at(request: WSGIRequest, pk: int) -> datetime.datetime:
    attachment = get_object_or_404(Attachment, pk=pk)
    return attachment.updated_at


@last_modified(get_updated_at)
def get_original(request: WSGIRequest, pk: int) -> HttpResponse:
    attachment = get_object_or_404(Attachment, pk=pk)
    return HttpResponseRedirect(attachment.original_file.url)


@last_modified(get_updated_at)
def get_processed(request: WSGIRequest, pk: int) -> HttpResponse:
    attachment = get_object_or_404(Attachment, pk=pk)
    return HttpResponseRedirect(attachment.processed_file.url)
