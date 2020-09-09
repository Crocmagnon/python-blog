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
            version = f.read().strip()[:8]
    except FileNotFoundError:
        version = "latest"
    return {"git_version": version}
