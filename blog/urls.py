"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from articles.views import api, feeds, html
from blog import settings

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="blog/robots.txt", content_type="text/plain"
        ),
    ),
    path("admin/", admin.site.urls),
    path("", html.ArticlesListView.as_view(), name="articles-list"),
    path("drafts/", html.DraftsListView.as_view(), name="drafts-list"),
    path("feed/", feeds.CompleteFeed(), name="complete-feed"),
    path("api/render/<int:article_pk>/", api.render_article, name="api-render-article"),
    path("<slug:slug>", html.ArticleDetailView.as_view(), name="article-detail-old"),
    path("<slug:slug>/", html.ArticleDetailView.as_view(), name="article-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
