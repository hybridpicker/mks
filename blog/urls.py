from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('uebersicht', views.blog_summary, name='blog_summary'),
    path('<slug>/', views.BlogPostView.as_view(), name='blog_post_detail'),
    path('neuer-eintrag', views.create_blog, name='create_blog_post'),
]
