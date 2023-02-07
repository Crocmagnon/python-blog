# Generated by Django 3.1 on 2020-08-18 19:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0014_auto_20200818_1952"),
    ]

    operations = [
        migrations.RemoveField(model_name="comment", name="approved"),
        migrations.AddField(
            model_name="comment",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
