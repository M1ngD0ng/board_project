from django.urls import path

from . import views
from .views import *

app_name: str = "boards"

urlpatterns: List = [
    path("", BoardListView.as_view(), name="board-list"),
    path(
        "<int:board_id>/",
        ArticleListView.as_view(),
        name="article-list",
    ),
    path("<int:board_id>/articles/", ArticleCreateView.as_view(), name="article-form"),
    path(
        "articles/<int:pk>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path(
        "articles/<int:pk>/update/",
        ArticleUpdateView.as_view(),
        name="article-update",
    ),
    path(
        "articles/<int:pk>/delete/",
        ArticleDeleteView.as_view(),
        name="article-delete",
    ),
    path(
        "articles/<int:article_id>/comment/",
        CommentCreateView.as_view(),
        name="comment-form",
    ),
]
