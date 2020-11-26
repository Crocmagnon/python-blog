import pytest
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from articles.models import Article, Page, User


def test_false():
    assert False


@pytest.mark.django_db
def test_can_access_list(
    client: Client, published_article: Article, published_page: Page
):
    res = client.get(reverse("articles-list"))
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    for art in [published_article, published_page]:
        assert art.title in content
    assert published_article.get_abstract() not in content
    assert published_page.get_formatted_content() not in content


@pytest.mark.django_db
def test_only_title_shown_on_list(client: Client, author: User):
    title = "This is a very long title mouahahaha"
    abstract = "Some abstract"
    after = "Some content after abstract"
    baker.make(
        Article,
        title=title,
        status=Article.PUBLISHED,
        author=author,
        content=f"{abstract}\n<!--more-->\n{after}",
    )  # type: Article
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert title in content
    assert abstract not in content
    assert after not in content


@pytest.mark.django_db
def test_access_article_by_slug(client: Client, published_article: Article):
    res = client.get(reverse("article-detail", kwargs={"slug": published_article.slug}))
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    assert published_article.title in content
    assert published_article.get_formatted_content() in content


@pytest.mark.django_db
def test_has_plausible_if_set(client: Client, settings):
    settings.PLAUSIBLE_DOMAIN = "gabnotes.org"
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert "https://plausible.augendre.info/js/plausible.js" in content
    assert 'data-domain="gabnotes.org"' in content


@pytest.mark.django_db
def test_doesnt_have_plausible_if_unset(client: Client, settings):
    settings.PLAUSIBLE_DOMAIN = None
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert "https://plausible.augendre.info/js/plausible.js" not in content


@pytest.mark.django_db
def test_logged_in_user_doesnt_have_plausible(client: Client, author: User, settings):
    client.force_login(author)
    settings.PLAUSIBLE_DOMAIN = "gabnotes.org"
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert "https://plausible.augendre.info/js/plausible.js" not in content
