from django.urls import path

from articles.views import api, feeds, html

urlpatterns = [
    path("", html.ArticlesListView.as_view(), name="articles-list"),
    path("drafts/", html.DraftsListView.as_view(), name="drafts-list"),
    path("feed/", feeds.CompleteFeed(), name="complete-feed"),
    path("api/render/<int:article_pk>/", api.render_article, name="api-render-article"),
    path("<slug:slug>/", html.ArticleDetailView.as_view(), name="article-detail"),
]
