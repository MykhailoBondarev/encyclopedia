from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("add", views.add_article, name="add"),
    path("edit/<str:title>", views.edit_article, name="edit"),
    path("random", views.random_article, name="random-article")
]
