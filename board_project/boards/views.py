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

from .forms import CommentForm
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
    template_name = "boards/article_detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        article = Article.objects.get(id=self.kwargs["article_id"])

        form.instance.article = article
        form.instance.author = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("boards:article-detail", kwargs={"pk": self.object.article.pk})
