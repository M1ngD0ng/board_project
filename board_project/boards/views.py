from typing import Any, Dict, List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm
from .models import *


class BoardListView(ListView):
    model: Board = Board
    template_name: str = "boards/board_list.html"
    context_object_name: str = "boards"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model: Article = Article
    fields: List[str] = ["title", "content"]
    template_name: str = "boards/article_form.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        board = Board.objects.get(id=self.kwargs["board_id"])
        form.instance.board = board
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["board"] = Board.objects.get(id=self.kwargs["board_id"])
        return context

    def get_success_url(self) -> str:
        return reverse("boards:article-detail", kwargs={"pk": self.object.pk})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model: Article = Article
    fields: List[str] = ["title", "content"]
    template_name: str = "boards/article_update.html"

    def get_success_url(self) -> str:
        return reverse("boards:article-detail", kwargs={"pk": self.object.pk})


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model: Article = Article

    def get_success_url(self) -> str:
        board_id = self.object.board.id
        return reverse_lazy("boards:article-list", kwargs={"board_id": board_id})

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        return redirect(self.get_object().get_absolute_url())


class ArticleDetailView(DetailView):
    model: Article = Article
    template_name: str = "boards/article_detail.html"
    context_object_name: str = "article"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class ArticleListView(ListView):
    model: Article = Article
    template_name: str = "boards/article_list.html"
    context_object_name: str = "articles"

    def get_queryset(self, **kwargs: Any) -> QuerySet[Article]:
        queryset = super().get_queryset(**kwargs)
        return (
            queryset.filter(board_id=self.kwargs["board_id"])
            .annotate(comment_count=Count("comments"))
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["board"] = Board.objects.get(id=self.kwargs["board_id"])
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model: Comment = Comment
    form_class: CommentForm = CommentForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        article = Article.objects.get(id=self.kwargs["article_id"])

        form.instance.article = article
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("boards:article-detail", kwargs={"pk": self.object.article.pk})
