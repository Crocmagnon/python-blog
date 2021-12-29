from typing import Any

from django.conf import settings
from django.http import HttpRequest

from articles.models import Article
from attachments.models import Attachment

IGNORED_PATHS = [
    "/robots.txt",
]


def drafts_count(request: HttpRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    if not request.user.is_authenticated:
        return {}
    return {"drafts_count": Article.objects.filter(status=Article.DRAFT).count()}


def date_format(request: HttpRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    return {"CUSTOM_ISO": r"Y-m-d\TH:i:sO", "ISO_DATE": "Y-m-d"}


def git_version(request: HttpRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    try:
        with open("/app/.version") as f:
            version = f.read().strip()
        url = settings.BLOG["repo"]["commit_url"].format(commit_sha=version)
        version = version[:8]
    except FileNotFoundError:
        version = "latest"
        url = settings.BLOG["repo"]["log"]
    return {"git_version": version, "git_version_url": url}


def analytics(request: HttpRequest) -> dict[str, Any]:
    return {
        "goatcounter_domain": settings.GOATCOUNTER_DOMAIN,
    }


def open_graph_image_url(request: HttpRequest) -> dict[str, Any]:
    if request.path in IGNORED_PATHS:
        return {}
    open_graph_image = Attachment.objects.get_open_graph_image()
    url = ""
    if open_graph_image:
        url = open_graph_image.processed_file.get_full_absolute_url(request)
    return {"open_graph_image_url": url}


def blog_metadata(request: HttpRequest) -> dict[str, Any]:
    return {
        "blog_title": settings.BLOG["title"],
        "blog_description": settings.BLOG["description"],
        "blog_author": settings.BLOG["author"],
        "blog_repo_homepage": settings.BLOG["repo"]["homepage"],
        "blog_status_url": settings.BLOG["status_url"],
    }
