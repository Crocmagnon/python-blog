# Generated by Django 3.1.5 on 2021-03-03 15:33
from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def forwards(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Tag = apps.get_model("articles", "Tag")
    Article = apps.get_model("articles", "Article")
    db_alias = schema_editor.connection.alias
    articles = Article.objects.using(db_alias).all()
    for article in articles:
        tags = []
        keyword: str
        for keyword in list(
            filter(None, (keyword.strip() for keyword in article.keywords.split(",")))
        ):
            tag = Tag.objects.using(db_alias).filter(name__iexact=keyword).first()
            if tag is None:
                tag = Tag.objects.create(name=keyword)
            tags.append(tag)
        article.tags.set(tags)
        article.keywords = ""
    Article.objects.bulk_update(articles, ["keywords"])


def backwards(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Article = apps.get_model("articles", "Article")
    db_alias = schema_editor.connection.alias
    articles = Article.objects.using(db_alias).all()
    for article in articles:
        article.keywords = ",".join(tag.name for tag in article.tags.all())
    Article.objects.bulk_update(articles, ["keywords"])


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0026_article_draft_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(related_name="articles", to="articles.Tag"),
        ),
        migrations.RunPython(forwards, backwards),
    ]
