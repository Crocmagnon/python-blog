import pytest

from articles.models import Article, User


@pytest.mark.django_db
def test_publish_article(unpublished_article: Article):
    assert unpublished_article.status == Article.DRAFT
    assert unpublished_article.published_at is None
    published_article = unpublished_article.publish()
    assert published_article.status == Article.PUBLISHED
    assert published_article.published_at is not None


@pytest.mark.django_db
def test_unpublish_article(published_article: Article):
    assert published_article.status == Article.PUBLISHED
    assert published_article.published_at is not None
    unpublished_article = published_article.unpublish()
    assert unpublished_article.status == Article.DRAFT
    assert unpublished_article.published_at is None


@pytest.mark.django_db
def test_save_article_adds_missing_slug(author: User):
    # Explicitly calling bulk_create with one article because it doesn't call save().
    articles = Article.objects.bulk_create(
        [Article(author=author, title="noice title", slug="", status=Article.DRAFT)]
    )
    article = articles[0]
    assert article.slug == ""
    article.save()
    assert article.slug != ""


@pytest.mark.django_db
def test_save_article_doesnt_change_existing_slug(published_article: Article):
    original_slug = published_article.slug
    published_article.title = "This is a brand new title"
    published_article.save()
    assert published_article.slug == original_slug
