# Generated by Django 3.1 on 2020-08-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="published_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
