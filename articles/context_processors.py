from django.conf import settings

from articles.models import Article, Page

IGNORED_PATHS = [
    "/robots.txt",
]


def pages(request):
    if request.path in IGNORED_PATHS:
        return {}
    return {"pages": Page.objects.filter(status=Article.PUBLISHED)}


def drafts_count(request):
    if request.path in IGNORED_PATHS:
        return {}
    return {"drafts_count": Article.objects.filter(status=Article.DRAFT).count()}


def date_format(request):
    if request.path in IGNORED_PATHS:
        return {}
    return {"CUSTOM_ISO": r"Y-m-d\TH:i:sO"}


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
