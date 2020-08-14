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
