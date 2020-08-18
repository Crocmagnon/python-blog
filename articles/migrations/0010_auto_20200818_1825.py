# Generated by Django 3.1 on 2020-08-18 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0009_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment", options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="comment",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]
