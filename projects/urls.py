from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('<slug>/', views.ProjectView.as_view(), name='project_view_detail'),
]
