import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import last_modified

from articles.models import Article


def get_article_last_modified(request: WSGIRequest, slug: str) -> datetime.datetime:
    key = request.GET.get("draft_key")
    qs = Article.objects.all().only("updated_at")
    if key:
        return get_object_or_404(qs, draft_key=key, slug=slug).updated_at
    if not request.user.is_authenticated:
        qs = qs.filter(status=Article.PUBLISHED)
    return get_object_or_404(qs, slug=slug).updated_at


@last_modified(get_article_last_modified)
def view_article(request: WSGIRequest, slug: str) -> HttpResponse:
    article = get_article(request, slug)
    if not request.user.is_authenticated:
        article.increment_view_count()
    context = {"article": article, "tags": article.tags.all()}
    return render(request, "articles/article_detail.html", context)


def get_article(request: WSGIRequest, slug: str) -> Article:
    key = request.GET.get("draft_key")
    qs = Article.objects.prefetch_related("tags")
    if key:
        return get_object_or_404(qs, draft_key=key, slug=slug)
    if not request.user.is_authenticated:
        qs = qs.filter(status=Article.PUBLISHED)
    return get_object_or_404(qs, slug=slug)
