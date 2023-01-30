import copy
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from articles.models import Article
from attachments.models import Attachment

IGNORED_PATHS = [
    "/robots.txt",
]


def drafts_count(request: WSGIRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    if not request.user.is_authenticated:
        return {}
    return {"drafts_count": Article.objects.filter(status=Article.DRAFT).count()}


def date_format(request: WSGIRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    return {"CUSTOM_ISO": r"Y-m-d\TH:i:sO", "ISO_DATE": "Y-m-d"}


def git_version(request: WSGIRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    try:
        with Path("/app/git/git-commit").open() as f:
            version = f.read().strip()
        url = settings.BLOG["repo"]["commit_url"].format(commit_sha=version)
        version = version[:8]
    except FileNotFoundError:
        version = "latest"
        url = settings.BLOG["repo"]["log"]
    return {"git_version": version, "git_version_url": url}


def analytics(_: WSGIRequest) -> dict[str, Any]:
    return {
        "goatcounter_domain": settings.GOATCOUNTER_DOMAIN,
    }


def open_graph_image_url(request: WSGIRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    open_graph_image = Attachment.objects.get_open_graph_image()
    url = ""
    if open_graph_image and open_graph_image.processed_file is not None:
        url = open_graph_image.processed_file.get_full_absolute_url(request)
    return {"open_graph_image_url": url}


def blog_metadata(_request: WSGIRequest) -> dict[str, Any]:
    blog_settings = copy.deepcopy(settings.BLOG)
    return {
        "blog": blog_settings,
    }
