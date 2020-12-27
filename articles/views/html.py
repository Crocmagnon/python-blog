from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views import generic

from articles.models import Article


class BaseArticleListView(generic.ListView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_title"] = settings.BLOG["title"]
        context["blog_description"] = settings.BLOG["description"]
        return context


class ArticlesListView(BaseArticleListView):
    model = Article
    context_object_name = "articles"
    queryset = Article.objects.filter(status=Article.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home_article = Article.objects.filter(
            status=Article.PUBLISHED, is_home=True
        ).first()  # type: Article
        context["article"] = home_article
        return context


class DraftsListView(LoginRequiredMixin, BaseArticleListView):
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
        key = self.request.GET.get("draft_key")
        if key:
            return Article.objects.filter(draft_key=key)

        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status=Article.PUBLISHED)
        return queryset

    def get_object(self, queryset=None) -> Article:
        obj = super().get_object(queryset)  # type: Article
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj
