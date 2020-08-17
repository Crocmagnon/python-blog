from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views import generic

from articles.models import Article


class ArticlesListView(generic.ListView):
    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["title"] = "Articles"
        return context

    def get_queryset(self):
        return super().get_queryset().filter(status=Article.PUBLISHED)


class DraftsListView(generic.ListView, LoginRequiredMixin):
    model = Article
    paginate_by = 15
    context_object_name = "articles"
    queryset = Article.with_pages.filter(status=Article.DRAFT)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["title"] = "Drafts"
        return context


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"
    queryset = Article.with_pages.all()
    template_name = "articles/article_detail.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset()
        return super().get_queryset().filter(status=Article.PUBLISHED)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, "page"):
            obj = obj.page
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj
