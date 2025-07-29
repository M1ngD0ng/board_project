from typing import Tuple

from django.contrib import admin

from ..models import Article, Board


class ArticleInline(admin.TabularInline):
    model: type = Article
    extra = 0
    fields: Tuple[str] = ("title", "content", "author", "created_at")
    readonly_fields: Tuple[str] = ("title", "content", "author", "created_at")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display: Tuple[str] = ("name", "description")
    inlines = (ArticleInline,)
