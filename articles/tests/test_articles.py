import pytest
from django.test import Client
from model_bakery import baker

from articles.models import Article, Page, User


@pytest.mark.django_db
def test_can_access_list(client: Client, author: User):
    article = baker.make(Article, author=author, status=Article.PUBLISHED)
    page = baker.make(Page, author=author, status=Article.PUBLISHED)
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
    baker.make(
        Article,
        status=Article.PUBLISHED,
        author=author,
        content=f"{abstract}\n<!--more-->\n{after}",
    )
    res = client.get("/")
    content = res.content.decode("utf-8")
    assert abstract in content
    assert after not in content
