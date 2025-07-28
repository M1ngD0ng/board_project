from django.db import models


class Board(models.Model):
    name: str = models.CharField(max_length=100)
    description: str = models.TextField()

    def __str__(self) -> str:
        return self.name
