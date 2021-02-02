
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="blogHome"),
    path("blogpost/<int:id2>", views.blogpost, name="blogPost")
]
