from datetime import datetime

from django.conf import settings
from django.db import models

from .article import Article


class Comment(models.Model):
    article: Article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author: "User" = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content: str = models.TextField()
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.author.username}의 댓글 : {self.content[:20]}"
