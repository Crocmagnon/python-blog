from typing import Union

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views import generic
from django.views.generic.edit import FormMixin

from articles.forms import CommentForm
from articles.models import Article, Comment, Page


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


class ArticleDetailView(FormMixin, generic.DetailView):
    model = Article
    form_class = CommentForm
    context_object_name = "article"
    queryset = Article.with_pages.all()
    template_name = "articles/article_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(status=Article.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        if hasattr(article, "article"):
            article = article.article
        context["comments"] = article.comments.filter(status=Comment.APPROVED)
        return context

    def get_object(self, queryset=None) -> Union[Article, Page]:
        obj = super().get_object(queryset)  # type: Article
        if hasattr(obj, "page"):
            obj = obj.page  # type: Page
        if not self.request.user.is_authenticated:
            obj.views_count = F("views_count") + 1
            obj.save(update_fields=["views_count"])

        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # type: Union[Article, Page]
        form = self.get_form()

        if not self.object.comments_allowed:
            messages.error(self.request, "Comments are disabled on this article.")
            # Bypassing self.form_invalid because we don't want its error message
            return super().form_invalid(form)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Your comment couldn\'t be saved, see <a href="#comment-form">the form below</a>.',
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        messages.success(
            self.request, "Comment successfully saved, pending review.",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
