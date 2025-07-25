from django.contrib import admin

from .models import Article, Board, Comment

admin.site.register(Board)
admin.site.register(Article)
admin.site.register(Comment)
