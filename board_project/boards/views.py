from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
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
    fields = ["title", "content"]
    template_name = "boards/article_form.html"

    def form_valid(self, form):
        board = Board.objects.get(id=self.kwargs["board_id"])
        form.instance.board = board
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = Board.objects.get(id=self.kwargs["board_id"])
        return context

    def get_success_url(self):
        return reverse("boards:article-detail", kwargs={"pk": self.object.pk})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "content"]
    template_name = "boards/article_update.html"

    def get_success_url(self):
        return reverse("boards:article-detail", kwargs={"pk": self.object.pk})


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article

    def get_success_url(self):
        board_id = self.object.board.id
        return reverse_lazy("boards:article-list", kwargs={"board_id": board_id})

    def get(self, request, *args, **kwargs):
        return redirect(self.get_object().get_absolute_url())


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = "article"


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
