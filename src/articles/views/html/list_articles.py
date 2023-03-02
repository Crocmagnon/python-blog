import operator
from functools import reduce
from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Page
from django.db.models import Q, QuerySet
from django.http import HttpResponseBase
from django.shortcuts import get_object_or_404
from django.views import generic

from articles.models import Article, Tag


class BaseArticleListView(generic.ListView):
    model = Article
    context_object_name = "articles"
    paginate_by = 10
    main_title = "Blog posts"
    html_title = ""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["blog_title"] = settings.BLOG["title"]
        context["blog_description"] = settings.BLOG["description"]
        page_obj: Page = context["page_obj"]
        if page_obj.has_next():
            querystring = self.build_querystring({"page": page_obj.next_page_number()})
            context["next_page_querystring"] = querystring
        if page_obj.has_previous():
            querystring = self.build_querystring(
                {"page": page_obj.previous_page_number()},
            )
            context["previous_page_querystring"] = querystring
        return context

    def get_additional_querystring_params(self) -> dict[str, str]:
        return {}

    def build_querystring(self, initial_queryparams: dict[str, Any]) -> str:
        querystring = {
            **initial_queryparams,
            **self.get_additional_querystring_params(),
        }
        return "&".join(f"{item[0]}={item[1]}" for item in querystring.items())


class PublicArticleListView(BaseArticleListView):
    queryset = Article.objects.filter(status=Article.PUBLISHED)


class ArticlesListView(PublicArticleListView):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        home_article = Article.objects.filter(
            status=Article.PUBLISHED,
            is_home=True,
        ).first()
        context["article"] = home_article
        return context


class SearchArticlesListView(PublicArticleListView):
    template_name = "articles/article_search.html"
    html_title = "Search"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_expression"] = self.request.GET.get("s") or ""
        return context

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        search_expression = self.request.GET.get("s")
        if not search_expression:
            return queryset.none()
        self.html_title = f"Search results for {search_expression}"
        search_terms = search_expression.split()
        return queryset.filter(
            reduce(operator.and_, (Q(title__icontains=term) for term in search_terms))
            | reduce(
                operator.and_,
                (Q(content__icontains=term) for term in search_terms),
            )
            | reduce(
                operator.and_,
                (Q(tags__name__icontains=term) for term in search_terms),
            ),
        ).distinct()

    def get_additional_querystring_params(self) -> dict[str, str]:
        search_expression = self.request.GET.get("s")
        if search_expression:
            return {"s": search_expression}
        return {}


class TagArticlesListView(PublicArticleListView):
    tag: Tag
    main_title = ""
    html_title = ""

    def dispatch(
        self,
        request: WSGIRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponseBase:
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        self.main_title = self.html_title = f"{self.tag.name} articles"
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["feed_title"] = self.tag.get_feed_title()
        context["feed_url"] = self.tag.get_feed_url()
        return context

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(tags=self.tag)


class DraftsListView(LoginRequiredMixin, BaseArticleListView):
    queryset = Article.objects.filter(status=Article.DRAFT)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Drafts"
        context["title_header"] = context["title"]
        return context
