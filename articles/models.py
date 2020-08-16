import re

import markdown
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Article(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    views_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_abstract(self):
        html = self.get_formatted_content()
        return html.split("<!--more-->")[0]

    def get_formatted_content(self):
        md = markdown.Markdown(extensions=["extra"])
        content = self.content
        content = re.sub(r"(\s)#(\w+)", r"\1\#\2", content)
        return md.convert(content)

    def publish(self, save=True):
        if not self.published_at:
            self.published_at = timezone.now()
        self.status = self.PUBLISHED
        if save:
            self.save()

    def unpublish(self, save=True):
        self.published_at = None
        self.status = self.DRAFT
        if save:
            self.save()
