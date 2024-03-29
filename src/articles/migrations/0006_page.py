# Generated by Django 3.1 on 2020-08-17 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0005_article_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "article_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="articles.article",
                    ),
                ),
            ],
            bases=("articles.article",),
        ),
    ]
