from typing import Union

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views import generic

from articles.models import Article, Page


class BaseArticleListView(generic.ListView):
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_title"] = settings.BLOG["title"]
        context["blog_description"] = settings.BLOG["description"]
        return context


class ArticlesListView(BaseArticleListView):
    model = Article
    context_object_name = "articles"
    queryset = Article.without_pages.filter(status=Article.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title_header"] = "Articles"
        return context


class DraftsListView(BaseArticleListView, LoginRequiredMixin):
    model = Article
    context_object_name = "articles"
    queryset = Article.objects.filter(status=Article.DRAFT)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Drafts"
        context["title_header"] = context["title"]
        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"
    template_name = "articles/article_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(status=Article.PUBLISHED)

    def get_object(self, queryset=None) -> Union[Article, Page]:
        obj = super().get_object(queryset)  # type: Article
        if hasattr(obj, "page"):
            obj = obj.page  # type: Page
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj
