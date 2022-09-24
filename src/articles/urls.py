from django.urls import path

from articles import views

urlpatterns = [
    path("", views.ArticlesListView.as_view(), name="articles-list"),
    path("drafts/", views.DraftsListView.as_view(), name="drafts-list"),
    path("search/", views.SearchArticlesListView.as_view(), name="search"),
    path("tag/<slug:slug>/feed/", views.TagFeed(), name="tag-feed"),
    path("tag/<slug:slug>/", views.TagArticlesListView.as_view(), name="tag"),
    path("feed/", views.CompleteFeed(), name="complete-feed"),
    path(
        "api/render/<int:article_pk>/", views.render_article, name="api-render-article"
    ),
    path("<slug:slug>/", views.view_article, name="article-detail"),
]
