# Generated by Django 3.1.1 on 2020-11-28 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attachments", "0004_auto_20200903_2116"),
    ]

    operations = [
        migrations.AddField(
            model_name="attachment",
            name="open_graph_image",
            field=models.BooleanField(blank=True, default=False),
            preserve_default=False,
        ),
    ]
