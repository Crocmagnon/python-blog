import os
import uuid

import pytest
from django.core.management import call_command
from django.utils import timezone

from articles.models import Article, Tag, User


@pytest.fixture()
@pytest.mark.django_db
def author() -> User:
    return User.objects.create_user("gaugendre", is_staff=True, is_superuser=True)


@pytest.fixture()
@pytest.mark.django_db
def tag() -> Tag:
    return Tag.objects.create(name="This is a new tag", slug="this-new-tag")


@pytest.fixture()
@pytest.mark.django_db
def published_article(author: User, tag: Tag) -> Article:
    article = Article.objects.create(
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
    article.tags.set([tag])
    return article


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
        draft_key=uuid.uuid4(),
    )


@pytest.fixture(autouse=True, scope="session")
def collect_static():
    call_command("collectstatic", "--no-input", "--clear")
