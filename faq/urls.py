from django.contrib import admin
from django.urls import path
from faq import views

urlpatterns = [
    path('faq', views.faq_view, name='faq_view'),
]
