import markdown
from django.contrib.auth.models import AbstractUser
from django.db import models


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

    class Meta:
        ordering = ["-published_at"]

    def get_abstract(self):
        md = markdown.Markdown(extensions=["extra"])
        html = md.convert(self.content)
        return html.split("<!--more-->")[0]

    def get_formatted_content(self):
        md = markdown.Markdown(extensions=["extra"])
        return md.convert(self.content)
