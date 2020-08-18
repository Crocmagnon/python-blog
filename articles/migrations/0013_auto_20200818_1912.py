# Generated by Django 3.1 on 2020-08-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0012_auto_20200818_1845"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.TextField(
                help_text="Your comment, limited to 500 characters. No formatting.",
                max_length=500,
            ),
        ),
    ]
