from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse

from .board import Board


class Article(models.Model):
    title: str = models.CharField(max_length=100)
    content: str = models.TextField()
    board: Board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    author: "User" = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"[{self.board.name}] {self.title}"

    def get_absolute_url(self) -> str:
        return reverse("boards:article-detail", kwargs={"pk": self.pk})
