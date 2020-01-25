from django.contrib import admin
from todo.models import Category, TodoList

# Register your models here.

admin.site.register(Category)
admin.site.register(TodoList)
