from typing import cast

from django.contrib import admin, messages
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

from .models import Article, Tag, User

admin.site.register(User, UserAdmin)


@register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ["status", "-published_at"]
    list_display = [
        "title",
        "status",
        "keywords",
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
                    ("author", "tags"),
                    ("status", "published_at"),
                    ("created_at", "updated_at"),
                    ("views_count",),
                    ("has_code", "has_custom_css"),
                ],
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
    search_fields = ["title", "content", "tags__name"]
    autocomplete_fields = ["tags"]
    show_full_result_count = False

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("tags")

    @admin.action(description="Publish selected articles")
    def publish(self, request: WSGIRequest, queryset: QuerySet) -> None:
        if not request.user.has_perm("articles.change_article"):
            messages.warning(request, "You're not allowed to do this.")
            return
        for article in queryset:
            article.publish()
        messages.success(request, f"{len(queryset)} articles published.")

    @admin.action(description="Unpublish selected articles")
    def unpublish(self, request: WSGIRequest, queryset: QuerySet) -> None:
        if not request.user.has_perm("articles.change_article"):
            messages.warning(request, "You're not allowed to do this.")
            return
        for article in queryset:
            article.unpublish()
        messages.success(request, f"{len(queryset)} articles unpublished.")

    @admin.action(description="Refresh draft key of selected articles")
    def refresh_draft_key(self, request: WSGIRequest, queryset: QuerySet) -> None:
        if not request.user.has_perm("articles.change_article"):
            messages.warning(request, "You're not allowed to do this.")
            return
        for article in queryset:
            article.refresh_draft_key()
        messages.success(request, f"{len(queryset)} draft keys refreshed.")

    actions = [publish, unpublish, refresh_draft_key]

    class Media:
        css = {
            "all": (
                "vendor/fonts/fira-code.css",
                "admin_articles.css",
            ),
        }

    def response_post_save_add(
        self,
        request: WSGIRequest,
        obj: Article,
    ) -> HttpResponseRedirect:
        if "_preview" in request.POST:
            return cast(HttpResponseRedirect, redirect("article-detail", slug=obj.slug))
        return super().response_post_save_add(request, obj)

    def response_change(self, request: WSGIRequest, obj: Article) -> HttpResponse:
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

    def change_view(
        self,
        request: WSGIRequest,
        object_id: int,
        form_url: str = "",
        extra_context: dict | None = None,
    ) -> HttpResponse:
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(
        self,
        request: WSGIRequest,
        form_url: str = "",
        extra_context: dict | None = None,
    ) -> HttpResponse:
        extra_context = extra_context or {}
        extra_context["show_save_and_add_another"] = False
        return super().add_view(request, form_url, extra_context)

    def read_time(self, instance: Article) -> str:
        return f"{instance.get_read_time()} min"

    @admin.display(boolean=True)
    def has_custom_css(self, instance: Article) -> bool:
        return bool(instance.custom_css)


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["slug", "name"]
    list_display_links = ["slug", "name"]
    prepopulated_fields = {"slug": ("name",)}
