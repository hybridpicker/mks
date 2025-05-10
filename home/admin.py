from django.contrib import admin
from .models import IndexText, Alert, NewsItem

# Register your models here
@admin.register(IndexText)
class IndexTextAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'message')

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'date_added', 'is_active', 'order')
    list_filter = ('is_active', 'icon')
    search_fields = ('title', 'content')
    ordering = ('-date_added', 'order')
    list_editable = ('is_active', 'order')
