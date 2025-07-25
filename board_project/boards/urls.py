from django.urls import path

from . import views
from .views import *

app_name = "boards"

urlpatterns = [
    path("", BoardListView.as_view(), name="board-list"),
    path(
        "<int:board_id>/",
        ArticleListView.as_view(),
        name="article-list",
    ),
]
