# Generated by Django 3.1.5 on 2021-03-06 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0030_tag_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="content",
            field=models.TextField(
                default='!!! warning "Draft"\n    This article is still a draft. It may appear by error in your feed if I click on the "publish" button too early 😊'
            ),
        ),
    ]
