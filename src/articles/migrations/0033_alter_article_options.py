# Generated by Django 4.0.4 on 2022-05-25 17:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0032_auto_20210306_1449"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-published_at", "-updated_at"]},
        ),
    ]
