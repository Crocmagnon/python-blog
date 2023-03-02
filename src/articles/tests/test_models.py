import pytest

from articles.models import Article, User


@pytest.mark.django_db()
def test_publish_article(unpublished_article: Article) -> None:
    assert unpublished_article.status == Article.DRAFT
    assert unpublished_article.published_at is None
    published_article = unpublished_article.publish()
    assert published_article.status == Article.PUBLISHED
    assert published_article.published_at is not None


@pytest.mark.django_db()
def test_unpublish_article(published_article: Article) -> None:
    assert published_article.status == Article.PUBLISHED
    assert published_article.published_at is not None
    unpublished_article = published_article.unpublish()
    assert unpublished_article.status == Article.DRAFT
    assert unpublished_article.published_at is None


@pytest.mark.django_db()
def test_save_article_adds_missing_slug(author: User) -> None:
    # Explicitly calling bulk_create with one article because it doesn't call save().
    articles = Article.objects.bulk_create(
        [Article(author=author, title="noice title", slug="", status=Article.DRAFT)],
    )
    article = articles[0]
    assert article.slug == ""
    article.save()
    assert article.slug != ""


@pytest.mark.django_db()
def test_save_article_doesnt_change_existing_slug(published_article: Article) -> None:
    original_slug = published_article.slug
    published_article.title = "This is a brand new title"
    published_article.save()
    assert published_article.slug == original_slug


@pytest.mark.django_db()
def test_empty_custom_css_minified(published_article: Article) -> None:
    published_article.custom_css = ""
    assert published_article.get_minified_custom_css == ""


@pytest.mark.django_db()
def test_simple_custom_css_minified(published_article: Article) -> None:
    published_article.custom_css = ".cls {\n    background-color:  red;\n}"
    assert published_article.get_minified_custom_css == ".cls{background-color:red}"


@pytest.mark.django_db()
def test_larger_custom_css_minified(published_article: Article) -> None:
    published_article.custom_css = """\
.profile {
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
}

.profile img {
    max-width: 200px;
    min-width: 100px;
    max-height: 200px;
    min-height: 100px;
    border-radius: 10%;
    padding: 1rem;
    flex-shrink: 1;
    flex-grow: 0;
    padding: 0;
}"""
    assert (
        published_article.get_minified_custom_css
        == ".profile{display:flex;justify-content:space-evenly;flex-wrap:wrap}.profile img{max-width:200px;min-width:100px;max-height:200px;min-height:100px;border-radius:10%;padding:1rem;flex-shrink:1;flex-grow:0;padding:0}"
    )
