import pytest
from django.template import Context, Template
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from articles.models import Article, User


@pytest.mark.django_db
def test_can_access_list(client: Client, published_article: Article):
    res = client.get(reverse("articles-list"))
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    assert published_article.title in content
    assert published_article.get_abstract() not in content


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
    _test_access_article_by_slug(client, published_article)


def _test_access_article_by_slug(client: Client, item: Article):
    res = client.get(reverse("article-detail", kwargs={"slug": item.slug}))
    _assert_article_is_rendered(item, res)


def _assert_article_is_rendered(item: Article, res):
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    assert item.title in content
    html = item.get_formatted_content
    assert html in content


@pytest.mark.django_db
def test_anonymous_cant_access_draft_detail(
    client: Client, unpublished_article: Article
):
    res = client.get(
        reverse("article-detail", kwargs={"slug": unpublished_article.slug})
    )
    assert res.status_code == 404


@pytest.mark.django_db
def test_anonymous_can_access_draft_detail_with_key(
    client: Client, unpublished_article: Article
):
    res = client.get(
        reverse("article-detail", kwargs={"slug": unpublished_article.slug})
        + f"?draft_key={unpublished_article.draft_key}"
    )
    _assert_article_is_rendered(unpublished_article, res)


@pytest.mark.django_db
def test_user_can_access_draft_detail(
    client: Client, author: User, unpublished_article: Article
):
    client.force_login(author)
    _test_access_article_by_slug(client, unpublished_article)


@pytest.mark.django_db
def test_anonymous_cant_access_drafts_list(
    client: Client, unpublished_article: Article
):
    res = client.get(reverse("drafts-list"))
    assert res.status_code == 302


@pytest.mark.django_db
def test_user_can_access_drafts_list(
    client: Client, author: User, unpublished_article: Article
):
    client.force_login(author)
    res = client.get(reverse("drafts-list"))
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    assert unpublished_article.title in content


@pytest.mark.django_db
def test_has_goatcounter_if_set(client: Client, settings):
    settings.GOATCOUNTER_DOMAIN = "gc.gabnotes.org"
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert "window.goatcounter" in content
    assert f"{settings.GOATCOUNTER_DOMAIN}/count" in content


@pytest.mark.django_db
def test_doesnt_have_goatcounter_if_unset(client: Client, settings):
    settings.GOATCOUNTER_DOMAIN = None
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert "window.goatcounter" not in content
    assert f"{settings.GOATCOUNTER_DOMAIN}/count" not in content


@pytest.mark.django_db
def test_logged_in_user_doesnt_have_goatcounter(client: Client, author: User, settings):
    client.force_login(author)
    settings.GOATCOUNTER_DOMAIN = "gc.gabnotes.org"
    res = client.get(reverse("articles-list"))
    content = res.content.decode("utf-8")
    assert "window.goatcounter" not in content
    assert f"{settings.GOATCOUNTER_DOMAIN}/count" not in content


@pytest.mark.django_db
def test_image_is_lazy(client: Client, published_article: Article):
    res = client.get(reverse("article-detail", kwargs={"slug": published_article.slug}))
    assert res.status_code == 200
    content = res.content.decode("utf-8")
    assert content.count('loading="lazy"') == 2
