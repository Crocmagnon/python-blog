import random
import uuid
from functools import cached_property

import rcssmin
import readtime
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
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
    author = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    views_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255)
    keywords = models.CharField(max_length=255, blank=True)
    has_code = models.BooleanField(default=False, blank=True)
    is_home = models.BooleanField(default=False, blank=True)
    custom_css = models.TextField(blank=True)
    draft_key = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title}"

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
        for keyword in self.get_formatted_keywords:
            potential_articles = Article.objects.filter(
                keywords__icontains=keyword,
                status=Article.PUBLISHED,
            ).exclude(pk=self.pk)
            for article in potential_articles:
                if keyword in article.get_formatted_keywords:
                    related_articles.add(article)
        sample_size = min([len(related_articles), 3])
        return random.sample(related_articles, sample_size)

    @cached_property
    def get_formatted_keywords(self):
        return list(
            filter(None, map(lambda k: k.strip().lower(), self.keywords.split(",")))
        )

    @cached_property
    def get_minified_custom_css(self):
        return rcssmin.cssmin(self.custom_css)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(
            "admin:%s_%s_change" % (content_type.app_label, content_type.model),
            args=(self.id,),
        )
