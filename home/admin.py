from django.contrib import admin
from home.models import IndexText, Alert
# Register your models here.


class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')  # Zeigt den Titel, Status und Erstellungsdatum
    list_filter = ('is_active', 'created_at')  # Filter nach Aktivität und Erstellungsdatum
    search_fields = ('title', 'message')  # Suche nach Titel und Nachricht


admin.site.register(IndexText)
admin.site.register(Alert, AlertAdmin)
