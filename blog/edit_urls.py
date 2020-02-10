from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('post/<id>', views.BlogPostEditView.as_view(), name='blog_post_edit_detail'),
    path('new', views.create_blog, name='create_blog_post'),
    path('summary', views.show_blogs_editing, name='show_blogs_editing'),
]
