from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('uebersicht', views.blog_summary, name='blog_summary'),
    path('<published_year>/<slug>/', views.BlogPostView.as_view(), name='blog_post_detail'),
    path('thanks', views.blog_thanks, name='blog_thanks'),
]
