import pytest
from django.utils import timezone

from articles.models import Article, User


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
        content=(
            "## some article markdown\n\n"
            "[an article link](https://article.com)\n"
            "![an image](https://article.com)\n"
            "![a referenced image][1]\n\n"
            "[1]: https://example.com/image.png"
        ),
    )


@pytest.fixture()
@pytest.mark.django_db
def unpublished_article(author: User) -> Article:
    return Article.objects.create(
        title="Some interesting article title, but sorry it is not public yet",
        status=Article.DRAFT,
        author=author,
        published_at=None,
        slug="some-draft-article-slug",
        content="## some draft article markdown\n\n[a draft article link](https://article.com)",
    )
