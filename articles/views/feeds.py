from django.contrib.syndication.views import Feed

from articles.models import Article
from blog import settings


class CompleteFeed(Feed):
    FEED_LIMIT = 15
    title = "Gab's Notes"
    link = settings.BLOG["base_url"]
    description = settings.BLOG["description"]

    def items(self):
        return Article.objects.filter(status=Article.PUBLISHED).order_by(
            "-published_at"
        )[: self.FEED_LIMIT]

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.get_formatted_content

    def item_pubdate(self, item: Article):
        return item.published_at
