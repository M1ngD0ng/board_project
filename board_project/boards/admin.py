from django.contrib import admin

from .models import Board, Category, Article, Comment

admin.site.register(Board)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
