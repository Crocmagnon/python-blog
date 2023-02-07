# Generated by Django 3.1.4 on 2020-12-27 18:43

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0025_article_custom_css"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="draft_key",
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
