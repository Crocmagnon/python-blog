import operator
from functools import reduce
from typing import Dict

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.views import generic

from articles.models import Article, Tag


class BaseArticleListView(generic.ListView):
    model = Article
    context_object_name = "articles"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_title"] = settings.BLOG["title"]
        context["blog_description"] = settings.BLOG["description"]
        page_obj = context["page_obj"]
        if page_obj.has_next():
            querystring = self.build_querystring({"page": page_obj.next_page_number()})
            context["next_page_querystring"] = querystring
        if page_obj.has_previous():
            querystring = self.build_querystring(
                {"page": page_obj.previous_page_number()}
            )
            context["previous_page_querystring"] = querystring
        return context

    def get_additional_querystring_params(self) -> Dict[str, str]:
        return dict()

    def build_querystring(self, initial_queryparams: Dict[str, str]) -> str:
        querystring = {
            **initial_queryparams,
            **self.get_additional_querystring_params(),
        }
        return "&".join(map(lambda item: f"{item[0]}={item[1]}", querystring.items()))


class PublicArticleListView(BaseArticleListView):
    queryset = Article.objects.filter(status=Article.PUBLISHED)


class ArticlesListView(PublicArticleListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home_article = Article.objects.filter(
            status=Article.PUBLISHED, is_home=True
        ).first()  # type: Article
        context["article"] = home_article
        return context


class SearchArticlesListView(PublicArticleListView):
    template_name = "articles/article_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_expression"] = self.request.GET.get("s") or ""
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_expression = self.request.GET.get("s")
        if not search_expression:
            return queryset.none()
        search_terms = search_expression.split()
        return queryset.filter(
            reduce(operator.and_, (Q(title__icontains=term) for term in search_terms))
            | reduce(
                operator.and_, (Q(content__icontains=term) for term in search_terms)
            )
            | reduce(
                operator.and_, (Q(tags__name__icontains=term) for term in search_terms)
            )
        ).distinct()

    def get_additional_querystring_params(self) -> Dict[str, str]:
        search_expression = self.request.GET.get("s")
        if search_expression:
            return {"s": search_expression}
        return {}


class TagArticlesListView(PublicArticleListView):
    tag = None

    def dispatch(self, request, *args, **kwargs):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_title"] = self.tag.get_feed_title()
        context["feed_url"] = self.tag.get_feed_url()
        return context

    def get_queryset(self):
        return super().get_queryset().filter(tags=self.tag)


class DraftsListView(LoginRequiredMixin, BaseArticleListView):
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
        key = self.request.GET.get("draft_key")
        if key:
            return Article.objects.filter(draft_key=key).prefetch_related("tags")

        queryset = super().get_queryset().prefetch_related("tags")
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status=Article.PUBLISHED)
        return queryset

    def get_object(self, queryset=None) -> Article:
        obj = super().get_object(queryset)  # type: Article
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj
