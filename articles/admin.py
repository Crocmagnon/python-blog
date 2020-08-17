from django import forms
from django.contrib import admin, messages
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.db import models

from .models import Article, Page, User

admin.site.register(User, UserAdmin)


@register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "author",
        "created_at",
        "published_at",
        "updated_at",
    ]
    list_display_links = ["title"]
    list_filter = ["status"]
    date_hierarchy = "created_at"
    fieldsets = [
        (
            "Metadata",
            {
                "fields": (
                    ("title", "slug"),
                    ("author", "status"),
                    ("published_at", "created_at", "updated_at"),
                    "views_count",
                )
            },
        ),
        ("Content", {"fields": ("content",)}),
    ]
    readonly_fields = ["created_at", "updated_at", "views_count"]
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"cols": "100", "rows": "50"})
        },
    }
    prepopulated_fields = {"slug": ("title",)}

    def publish(self, request, queryset):
        if not request.user.has_perm("articles.change_article"):
            messages.warning(request, "You're not allowed to do this.")
            return
        for article in queryset:
            article.publish()
        messages.success(request, f"{len(queryset)} articles published.")

    publish.short_description = "Publish selected articles"

    def unpublish(self, request, queryset):
        if not request.user.has_perm("articles.change_article"):
            messages.warning(request, "You're not allowed to do this.")
            return
        for article in queryset:
            article.unpublish()
        messages.success(request, f"{len(queryset)} articles unpublished.")

    unpublish.short_description = "Unpublish selected articles"
    actions = [publish, unpublish]

    class Media:
        css = {"all": ("admin_articles.css",)}


@register(Page)
class PageAdmin(ArticleAdmin):
    list_display = ["position"] + ArticleAdmin.list_display
    fieldsets = [
        (
            "Metadata",
            {
                "fields": (
                    ("title", "slug", "position"),
                    ("author", "status"),
                    ("published_at", "created_at", "updated_at"),
                    "views_count",
                )
            },
        ),
        ("Content", {"fields": ("content",)}),
    ]
