import re
import uuid
from functools import cached_property

import html2text
import markdown
import readtime
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from markdown.extensions.codehilite import CodeHiliteExtension

from articles.markdown import LazyLoadingImageExtension
from articles.utils import build_full_absolute_url


class User(AbstractUser):
    pass


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
        converter = html2text.HTML2Text()
        converter.ignore_images = True
        converter.ignore_links = True
        converter.ignore_tables = True
        converter.ignore_emphasis = True
        text = converter.handle(html)
        total_length = 0
        text_result = []
        for word in text.split():
            if len(word) + 1 + total_length > 160:
                break
            text_result.append(word)
            total_length += len(word) + 1
        return " ".join(text_result) + "..."

    @cached_property
    def get_formatted_content(self):
        md = markdown.Markdown(
            extensions=[
                "extra",
                CodeHiliteExtension(linenums=False, guess_lang=False),
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
        return readtime.of_html(self.get_formatted_content).minutes
