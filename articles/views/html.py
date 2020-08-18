from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect
from django.views import generic

from articles.forms import CommentForm
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
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(status=Article.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = self.object
        if hasattr(article, "article"):
            article = article.article
        context["comments"] = article.comments.filter(approved=True)
        context["comment_form"] = CommentForm()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, "page"):
            obj = obj.page
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj


class CreateCommentView(generic.CreateView):
    model = Article
    form_class = CommentForm

    def form_valid(self, form):
        self.object = self.get_object()
        self.comment = form.save(commit=False)
        self.comment.article = self.object
        self.comment.save()
        messages.success(self.request, "Comment successfully saved.")
        return HttpResponseRedirect(self.get_success_url())
