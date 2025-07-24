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
