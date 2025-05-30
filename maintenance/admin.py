from django.contrib import admin
from .models import MaintenanceMode

@admin.register(MaintenanceMode)
class MaintenanceModeAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'title', 'updated_at']
    fields = ['is_active', 'title', 'message', 'expected_downtime']
    
    def has_add_permission(self, request):
        # Nur eine Instanz erlauben
        return MaintenanceMode.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Löschen verhindern
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Direkt zur Änderungsansicht weiterleiten wenn Objekt existiert
        obj = MaintenanceMode.load()
        return self.changeform_view(request, object_id=str(obj.pk), extra_context=extra_context)