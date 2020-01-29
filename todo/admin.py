from django.contrib import admin
from todo.models import Category, TodoList, FinishedItems

# Register your models here.

admin.site.register(Category)
admin.site.register(TodoList)
admin.site.register(FinishedItems)
