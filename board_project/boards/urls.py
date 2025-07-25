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
    path(
        "<int:board_id>/articles/", ArticleCreateView.as_view(), name="article-create"
    ),
    path(
        "<int:board_id>/articles/<int:article_id>",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path(
        "<int:board_id>/articles/<int:article_id>",
        ArticleUpdateView.as_view(),
        name="article-update",
    ),
    path(
        "<int:board_id>/articles/<int:article_id>",
        ArticleDeleteView.as_view(),
        name="article-delete",
    ),
]
