from django.conf import settings

from articles.models import Article
from attachments.models import Attachment

IGNORED_PATHS = [
    "/robots.txt",
]


def drafts_count(request):
    if request.path in IGNORED_PATHS:
        return {}
    return {"drafts_count": Article.objects.filter(status=Article.DRAFT).count()}


def date_format(request):
    if request.path in IGNORED_PATHS:
        return {}
    return {"CUSTOM_ISO": r"Y-m-d\TH:i:sO", "ISO_DATE": "Y-m-d"}


def git_version(request):
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


def plausible(request):
    return {"plausible_domain": settings.PLAUSIBLE_DOMAIN}


def open_graph_image_url(request):
    if request.path in IGNORED_PATHS:
        return {}
    open_graph_image = Attachment.objects.get_open_graph_image()
    url = ""
    if open_graph_image:
        url = open_graph_image.processed_file.get_full_absolute_url(request)
    return {"open_graph_image_url": url}


def blog_metadata(request):
    context = {}
    context["blog_title"] = settings.BLOG["title"]
    context["blog_description"] = settings.BLOG["description"]
    context["blog_author"] = settings.BLOG["author"]
    return context
