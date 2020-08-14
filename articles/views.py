from django.db.models import F
from django.views import generic

from articles.models import Article


class ArticlesListView(generic.ListView):
    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get_queryset(self):
        return super().get_queryset().filter(status=Article.PUBLISHED)


class ArticleDetailView(generic.DetailView):
    model = Article
    context_object_name = "article"

    def get_queryset(self):
        return super().get_queryset().filter(status=Article.PUBLISHED)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj
