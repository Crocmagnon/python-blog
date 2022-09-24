from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from articles.models import Article


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
