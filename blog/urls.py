from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('gitarre', views.blog_guitar_summary, name='blog_guitar_summary'),
    path('<slug>/', views.BlogPostView.as_view(), name='blog_post_detail'),
]
