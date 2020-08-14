from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import Article, User

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
                    "title",
                    ("author", "status"),
                    ("published_at", "created_at", "updated_at"),
                    "views_count",
                )
            },
        ),
        ("Content", {"fields": ("content",)}),
    ]
    readonly_fields = ["created_at", "updated_at", "views_count"]
