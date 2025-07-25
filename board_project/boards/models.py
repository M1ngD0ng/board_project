from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.board.name}] {self.title}"

    def get_absolute_url(self):
        return reverse("boards:article-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}의 댓글 : {self.content[:20]}"
