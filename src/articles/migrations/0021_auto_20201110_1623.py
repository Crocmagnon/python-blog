# Generated by Django 3.1.1 on 2020-11-10 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0020_auto_20200903_2157"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="comments_allowed",
        ),
        migrations.DeleteModel(
            name="Comment",
        ),
    ]