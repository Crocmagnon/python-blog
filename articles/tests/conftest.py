import pytest
from django.utils import timezone

from articles.models import Article, Page, User


@pytest.fixture()
@pytest.mark.django_db
def author():
    return User.objects.create_user("gaugendre")


@pytest.fixture()
@pytest.mark.django_db
def published_article(author):
    return Article.objects.create(
        title="Some interesting title",
        status=Article.PUBLISHED,
        author=author,
        published_at=timezone.now(),
        slug="some-slug",
        content="# some markdown\n\n[a link](https://example.com)",
    )


@pytest.fixture()
@pytest.mark.django_db
def published_page(author):
    return Page.objects.create(
        title="Some interesting title",
        status=Article.PUBLISHED,
        author=author,
        published_at=timezone.now(),
        slug="some-slug",
        content="# some markdown\n\n[a link](https://example.com)",
    )
