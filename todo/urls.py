from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('todo', views.todo_view, name='todo_view'),
    path('todo/categories', views.todo_categories_view, name='todo_categories_view'),
]
