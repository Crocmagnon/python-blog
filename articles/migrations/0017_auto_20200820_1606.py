# Generated by Django 3.1 on 2020-08-20 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0016_comment_user_notified"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment", options={"ordering": ["-created_at"]},
        ),
    ]