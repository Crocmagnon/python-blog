import re

import markdown
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import HttpRequest
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from markdown.extensions.codehilite import CodeHiliteExtension

from articles.markdown import LazyLoadingImageExtension


class User(AbstractUser):
    pass


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(page__isnull=True)


class AdminUrlMixin:
    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )


class Article(AdminUrlMixin, models.Model):
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
    author = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    views_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255)
    comments_allowed = models.BooleanField(default=True)

    objects = ArticleManager()
    with_pages = models.Manager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        type_ = "Article"
        if hasattr(self, "page"):
            type_ = "Page"
        return f"{self.title} ({type_})"

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})

    def get_full_absolute_url(self, request: HttpRequest = None):
        url = self.get_absolute_url()
        if request:
            return request.build_absolute_uri(url)
        else:
            return (settings.BLOG["base_url"] + url).replace("//", "/")

    def get_abstract(self):
        html = self.get_formatted_content()
        return html.split("<!--more-->")[0]

    def get_formatted_content(self):
        md = markdown.Markdown(
            extensions=[
                "extra",
                CodeHiliteExtension(linenums=False),
                LazyLoadingImageExtension(),
            ]
        )
        content = self.content
        content = re.sub(r"(\s)#(\w+)", r"\1\#\2", content)
        return md.convert(content)

    def publish(self):
        if not self.published_at:
            self.published_at = timezone.now()
        self.status = self.PUBLISHED
        self.save()

    def unpublish(self):
        self.published_at = None
        self.status = self.DRAFT
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Page(Article):
    objects = models.Manager()
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ["position", "-published_at"]


class Comment(AdminUrlMixin, models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )
    username = models.CharField(
        max_length=255, help_text="Will be displayed with your comment."
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text=(
            "Not mandatory, fill only if you want me to be able to contact you. "
            "It will never be displayed here nor shared with any third party."
        ),
    )
    content = models.TextField(
        max_length=500,
        help_text="Your comment, limited to 500 characters. No formatting.",
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    user_notified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.username} - {self.content[:50]}"

    def get_absolute_url(self):
        return self.article.get_absolute_url() + "#" + str(self.id)

    def get_full_absolute_url(self, request: HttpRequest = None):
        return self.article.get_full_absolute_url(request) + "#" + str(self.id)
