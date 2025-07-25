from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import *


def index(request):
    return HttpResponse("Hello World!")


class BoardListView(ListView):
    model = Board
    template_name = "boards/board_list.html"
    context_object_name = "boards"


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
    template_name = "boards/article_list.html"
    context_object_name = "articles"

    def get_queryset(self, **kwargs):
        return Article.objects.filter(board=self.kwargs["board_id"]).order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = Board.objects.get(id=self.kwargs["board_id"])
        return context
