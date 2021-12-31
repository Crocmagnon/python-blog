import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from articles.models import Article, User
from articles.views.feeds import CompleteFeed


@pytest.mark.django_db()
def test_can_access_feed(client: Client, published_article: Article) -> None:
    res = client.get(reverse("complete-feed"))
    assert res.status_code == 200
    assert "application/rss+xml" in res["content-type"]
    content = res.content.decode("utf-8")
    assert published_article.title in content


@pytest.mark.django_db()
def test_feed_limits_number_of_articles(client: Client, author: User) -> None:
    baker.make(Article, 100, status=Article.PUBLISHED, author=author)
    res = client.get(reverse("complete-feed"))
    content = res.content.decode("utf-8")
    assert content.count("<item>") == CompleteFeed.FEED_LIMIT
