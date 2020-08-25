from articles.models import Article, Page


def pages(request):
    return {"pages": Page.objects.filter(status=Article.PUBLISHED)}


def drafts_count(request):
    return {"drafts_count": Article.with_pages.filter(status=Article.DRAFT).count()}


def date_format(request):
    return {"CUSTOM_ISO": r"Y-m-d\TH:i:sO"}
