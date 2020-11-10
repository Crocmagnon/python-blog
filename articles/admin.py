import copy

from django.contrib import admin, messages
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect

from .models import Article, Page, User

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
    ]
    list_display_links = ["title"]
    list_filter = ["status"]
    date_hierarchy = "created_at"
    fieldsets = [
        (
            "Metadata",
            {
                "fields": [
                    ("title", "slug"),
                    ("author",),
                    ("status", "published_at"),
                    ("created_at", "updated_at"),
                    "views_count",
                ]
            },
        ),
        ("Content", {"fields": ("content",)}),
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "views_count",
        "status",
        "published_at",
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
    actions = [publish, unpublish]

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


@register(Page)
class PageAdmin(ArticleAdmin):
    list_display = ["position"] + ArticleAdmin.list_display

    def get_fieldsets(self, request, obj=None):
        article_fieldsets = copy.deepcopy(ArticleAdmin.fieldsets)
        article_fieldsets[0][1]["fields"][0] = ("title", "slug", "position")
        return article_fieldsets
