# Generated by Django 3.1.3 on 2020-12-24 16:46
from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def forwards_func(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Article = apps.get_model("articles", "Article")
    db_alias = schema_editor.connection.alias
    Article.objects.using(db_alias).filter(slug="about-me").update(is_home=True)


def reverse_func(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0023_article_has_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="is_home",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.DeleteModel(
            name="Page",
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
