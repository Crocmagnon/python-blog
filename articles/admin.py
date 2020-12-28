import copy

from django.contrib import admin, messages
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect

from .models import Article, User

admin.site.register(User, UserAdmin)


@register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ["status", "-published_at"]
    list_display = [
        "title",
        "status",
        "author",
        "created_at",
        "published_at",
        "updated_at",
        "views_count",
        "has_code",
        "is_home",
        "has_custom_css",
        "read_time",
    ]
    list_display_links = ["title"]
    list_filter = [
        "status",
        "has_code",
        "status",
        "is_home",
    ]
    date_hierarchy = "created_at"
    fieldsets = [
        (
            "Metadata",
            {
                "fields": [
                    ("title", "slug"),
                    ("author", "keywords"),
                    ("status", "published_at"),
                    ("created_at", "updated_at"),
                    ("views_count", "read_time"),
                    ("has_code", "has_custom_css"),
                ]
            },
        ),
        (
            "Content",
            {"fields": ("content",)},
        ),
        (
            "Custom CSS",
            {
                "fields": ("custom_css",),
                "classes": ("collapse",),
            },
        ),
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "views_count",
        "status",
        "published_at",
        "read_time",
        "has_custom_css",
    ]
    prepopulated_fields = {"slug": ("title",)}
    change_form_template = "articles/article_change_form.html"

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

    def refresh_draft_key(self, request, queryset):
        if not request.user.has_perm("articles.change_article"):
            messages.warning(request, "You're not allowed to do this.")
            return
        for article in queryset:
            article.refresh_draft_key()
        messages.success(request, f"{len(queryset)} draft keys refreshed.")

    refresh_draft_key.short_description = "Refresh draft key of selected articles"
    actions = [publish, unpublish, refresh_draft_key]

    class Media:
        css = {"all": ("admin_articles.css",)}

    def response_post_save_add(self, request, obj: Article):
        if "_preview" in request.POST:
            return redirect("article-detail", slug=obj.slug)
        return super().response_post_save_add(request, obj)

    def response_change(self, request, obj: Article):
        if "_preview" in request.POST:
            obj.save()
            return redirect("article-detail", slug=obj.slug)
        if "_publish" in request.POST:
            obj.publish()
            messages.success(request, "Item has been published")
            return redirect(".")
        if "_unpublish" in request.POST:
            obj.unpublish()
            messages.success(request, "Item has been unpublished")
            return redirect(".")
        return super().response_change(request, obj)

    def read_time(self, instance: Article):
        return f"{instance.get_read_time()} min"

    def has_custom_css(self, instance: Article):
        return bool(instance.custom_css)

    has_custom_css.boolean = True
