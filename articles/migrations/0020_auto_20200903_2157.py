# Generated by Django 3.1 on 2020-09-03 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0019_article_comments_allowed"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment", options={"ordering": ["created_at"]}
        ),
    ]
