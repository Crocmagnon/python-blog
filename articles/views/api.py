from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from articles.models import Article


@login_required
@require_POST
def render_article(request, article_pk):
    template = "articles/article_detail.html"
    article = Article.objects.get(pk=article_pk)
    article.content = request.POST.get("content", article.content)
    article.title = request.POST.get("title", article.title)
    article.custom_css = request.POST.get("custom_css", article.custom_css)
    has_code = request.POST.get("has_code")
    if has_code is not None:
        article.has_code = has_code == "true"
    html = render(request, template, context={"article": article})
    return HttpResponse(html)
