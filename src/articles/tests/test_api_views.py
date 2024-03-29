import pytest
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse

from articles.models import Article
from articles.utils import format_article_content


@pytest.mark.django_db()
def test_unauthenticated_render_redirects(
    published_article: Article,
    client: Client,
) -> None:
    api_res = client.post(
        reverse("api-render-article", kwargs={"article_pk": published_article.pk}),
        data={"content": published_article.content},
    )
    assert api_res.status_code == 302


@pytest.mark.django_db()
def test_render_article_same_content(
    published_article: Article,
    client: Client,
) -> None:
    client.force_login(published_article.author)
    api_res = post_article(client, published_article, published_article.content)
    standard_res = client.get(
        reverse("article-detail", kwargs={"slug": published_article.slug}),
    )
    assert api_res.status_code == 200
    assert standard_res.status_code == 200
    # ignore an expected difference
    api_content: str = api_res.content.decode("utf-8")
    standard_content: str = standard_res.content.decode("utf-8")
    api_content = api_content.replace(
        "/api/render/1/",
        "/some-article-slug/",
    )

    assert api_content == standard_content


@pytest.mark.django_db()
def test_render_article_change_content(
    published_article: Article,
    client: Client,
) -> None:
    client.force_login(published_article.author)
    preview_content = "This is a different content **with strong emphasis**"
    api_res = post_article(client, published_article, preview_content)
    assert api_res.status_code == 200
    api_content: str = api_res.content.decode("utf-8")
    html_preview_content = format_article_content(preview_content)
    assert html_preview_content in api_content


@pytest.mark.django_db()
def test_render_article_doesnt_save(published_article: Article, client: Client) -> None:
    client.force_login(published_article.author)
    original_content = published_article.content
    preview_content = "This is a different content **with strong emphasis**"
    api_res = post_article(client, published_article, preview_content)
    assert api_res.status_code == 200
    published_article.refresh_from_db()
    assert published_article.content == original_content


@pytest.mark.django_db()
def test_render_article_no_tags(published_article: Article, client: Client) -> None:
    client.force_login(published_article.author)
    api_res = client.post(
        reverse("api-render-article", kwargs={"article_pk": published_article.pk}),
        data={"content": published_article.content, "tag_ids": ""},
    )
    assert api_res.status_code == 200


def post_article(client: Client, article: Article, content: str) -> HttpResponse:
    return client.post(
        reverse("api-render-article", kwargs={"article_pk": article.pk}),
        data={
            "content": content,
            "tag_ids": ",".join(
                map(str, article.tags.all().values_list("pk", flat=True)),
            ),
        },
    )
