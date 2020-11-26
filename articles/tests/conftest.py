import pytest
from django.utils import timezone

from articles.models import Article, Page, User


@pytest.fixture()
@pytest.mark.django_db
def author() -> User:
    return User.objects.create_user("gaugendre")


@pytest.fixture()
@pytest.mark.django_db
def published_article(author: User) -> Article:
    return Article.objects.create(
        title="Some interesting article title",
        status=Article.PUBLISHED,
        author=author,
        published_at=timezone.now(),
        slug="some-article-slug",
        content="## some article markdown\n\n[an article link](https://article.com)",
    )


@pytest.fixture()
@pytest.mark.django_db
def published_page(author: User) -> Page:
    return Page.objects.create(
        title="Some interesting page title",
        status=Article.PUBLISHED,
        author=author,
        published_at=timezone.now(),
        slug="some-page-slug",
        content="## some page markdown\n\n[a page link](https://page.com)",
        position=2,
    )
