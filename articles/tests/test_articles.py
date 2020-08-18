import pytest
from django.test import Client
from django.utils import timezone

from articles.models import Article, Page, User


@pytest.mark.django_db
def test_can_access_list(client: Client, author: User):
    article = Article.objects.create(
        author=author,
        title="Sample published",
        status=Article.PUBLISHED,
        published_at=timezone.now(),
        slug="sample-published",
        content="Some content lorem ipsum",
    )
    page = Page.objects.create(
        author=author,
        title="Sample page published",
        status=Article.PUBLISHED,
        published_at=timezone.now(),
        slug="sample-page-published",
        content="Some page content lorem ipsum",
    )
    res = client.get("/")
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    for art in [article, page]:
        assert art.title in content
    assert article.content in content
    assert page.content not in content


@pytest.mark.django_db
def test_abstract_shown_on_list(client: Client, author: User):
    abstract = "Some abstract"
    after = "Some content after abstract"
    article = Article.objects.create(
        author=author,
        title="Sample published",
        status=Article.PUBLISHED,
        published_at=timezone.now(),
        slug="sample-published",
        content=f"{abstract}\n<!--more-->\n{after}",
    )
    res = client.get("/")
    content = res.content.decode("utf-8")
    assert abstract in content
    assert after not in content
