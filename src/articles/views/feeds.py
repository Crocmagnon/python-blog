from django.contrib.syndication.views import Feed

from articles.models import Article, Tag
from blog import settings


class CompleteFeed(Feed):
    FEED_LIMIT = 15
    title = settings.BLOG["title"]
    link = settings.BLOG["base_url"]
    description = settings.BLOG["description"]

    def get_queryset(self, obj):
        return Article.objects.filter(status=Article.PUBLISHED).order_by(
            "-published_at"
        )

    def items(self, obj):
        return self.get_queryset(obj)[: self.FEED_LIMIT]

    def item_description(self, item: Article):
        return item.get_formatted_content

    def item_pubdate(self, item: Article):
        return item.published_at


class TagFeed(CompleteFeed):
    def get_object(self, request, *args, **kwargs):
        return Tag.objects.get(slug=kwargs.get("slug"))

    def get_queryset(self, tag):
        return super().get_queryset(tag).filter(tags=tag)

    def title(self, tag):
        return tag.get_feed_title()

    def link(self, tag):
        return tag.get_absolute_url()
