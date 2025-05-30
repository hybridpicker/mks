from .models import MaintenanceMode

def maintenance_context(request):
    """
    Context Processor um Maintenance Status in allen Templates verfügbar zu machen
    """
    maintenance = MaintenanceMode.load()
    return {
        'maintenance_mode': maintenance.is_active,
        'is_superuser': request.user.is_authenticated and request.user.is_superuser,
    }