from datetime import datetime
from typing import Iterable

from django.contrib.syndication.views import Feed
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from articles.models import Article, Tag
from blog import settings


class BaseFeed(Feed):
    FEED_LIMIT = 15
    description = settings.BLOG["description"]

    def item_description(self, item: Article) -> str:  # type: ignore[override]
        return item.get_formatted_content

    def item_pubdate(self, item: Article) -> datetime | None:
        return item.published_at

    def _get_queryset(self) -> QuerySet[Article]:
        return Article.objects.filter(status=Article.PUBLISHED).order_by(
            "-published_at"
        )


class CompleteFeed(BaseFeed):
    title = settings.BLOG["title"]
    link = settings.BLOG["base_url"]

    def items(self) -> Iterable[Article]:
        return self._get_queryset()[: self.FEED_LIMIT]


class TagFeed(BaseFeed):
    def get_object(  # type: ignore[override]
        self, request: WSGIRequest, *args, **kwargs
    ) -> Tag:
        return Tag.objects.get(slug=kwargs.get("slug"))

    def title(self, tag: Tag) -> str:
        return tag.get_feed_title()

    def link(self, tag: Tag) -> str:
        return tag.get_absolute_url()

    def items(self, tag: Tag) -> Iterable[Article]:
        return self._get_queryset().filter(tags=tag)[: self.FEED_LIMIT]
