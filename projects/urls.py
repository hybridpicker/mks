from django.contrib import admin
from django.urls import include, re_path, path

from . import views

urlpatterns = [
    path('<slug>/', views.ProjectView.as_view(), name='project_view_detail'),
]
