from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('formulare', views.pdf_forms_view, name='pdf_forms_view'),
]
