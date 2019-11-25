from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('galerie', views.gallery_view, name='gallery_view'),
]
