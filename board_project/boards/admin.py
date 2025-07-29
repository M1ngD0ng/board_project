from django.contrib import admin

from .models import Article, Board, Comment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at"]
    list_filter = ["board", "author"]
    search_fields = ["title", "content"]
