import random
import uuid
from functools import cached_property

import rcssmin
import readtime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Prefetch
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from articles.utils import (
    build_full_absolute_url,
    format_article_content,
    get_html_to_text_converter,
    truncate_words_after_char_count,
)


class User(AbstractUser):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag", kwargs={"slug": self.slug})

    def get_feed_title(self):
        return f"{self.name} - {settings.BLOG['title']}"

    def get_feed_url(self):
        return reverse("tag-feed", kwargs={"slug": self.slug})


class Article(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
    ]
    CONTENT_DEFAULT = (
        '!!! warning "Draft"\n'
        "    This article is still a draft. It may appear by error in your feed "
        'if I click on the "publish" button too early 😊'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(default=CONTENT_DEFAULT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    views_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255)
    has_code = models.BooleanField(default=False, blank=True)
    is_home = models.BooleanField(default=False, blank=True)
    custom_css = models.TextField(blank=True)
    draft_key = models.UUIDField(default=uuid.uuid4)
    tags = models.ManyToManyField(to=Tag, related_name="articles", blank=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})

    def get_abstract(self):
        html = self.get_formatted_content
        return html.split("<!--more-->")[0]

    @cached_property
    def get_description(self):
        html = self.get_formatted_content
        converter = get_html_to_text_converter()
        text = converter.handle(html)
        return truncate_words_after_char_count(text, 160)

    @cached_property
    def get_formatted_content(self):
        return format_article_content(self.content)

    def publish(self):
        if not self.published_at:
            self.published_at = timezone.now()
        self.status = self.PUBLISHED
        self.save()
        return self

    def unpublish(self):
        self.published_at = None
        self.status = self.DRAFT
        self.save()
        return self

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def draft_public_url(self):
        url = self.get_absolute_url() + f"?draft_key={self.draft_key}"
        return build_full_absolute_url(request=None, url=url)

    def refresh_draft_key(self):
        self.draft_key = uuid.uuid4()
        self.save()

    def get_read_time(self):
        content = self.get_formatted_content
        if content:
            return readtime.of_html(content).minutes
        return 0

    @cached_property
    def get_related_articles(self):
        related_articles = set()
        published_articles = Article.objects.filter(status=Article.PUBLISHED)
        for tag in self.tags.all().prefetch_related(
            Prefetch("articles", published_articles, to_attr="published_articles")
        ):
            related_articles.update(tag.published_articles)
        sample_size = min([len(related_articles), 3])
        return random.sample(list(related_articles), sample_size)

    @cached_property
    def keywords(self):
        return ", ".join(map(lambda tag: tag.name, self.tags.all()))

    @cached_property
    def get_minified_custom_css(self):
        return rcssmin.cssmin(self.custom_css)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            f"admin:{content_type.app_label}_{content_type.model}_change",
            args=(self.id,),
        )
