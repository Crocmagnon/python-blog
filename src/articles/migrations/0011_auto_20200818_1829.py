# Generated by Django 3.1 on 2020-08-18 16:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0010_auto_20200818_1825"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment", old_name="active", new_name="approved"
        ),
    ]
