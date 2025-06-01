from .models import MaintenanceMode
from django.core.cache import cache
import os

def maintenance_mode(request):
    """
    Context Processor um Maintenance Status in allen Templates verfügbar zu machen
    """
    # Prüfe verschiedene Quellen für Maintenance Status
    maintenance_active = False
    
    # 1. Environment Variable
    if os.environ.get('MAINTENANCE_MODE', 'false').lower() == 'true':
        maintenance_active = True
    else:
        # 2. Cache
        cached_status = cache.get('maintenance_mode_status')
        if cached_status is not None:
            maintenance_active = cached_status
        else:
            # 3. Datenbank
            try:
                maintenance = MaintenanceMode.load()
                maintenance_active = maintenance.is_active
                # Cache für 60 Sekunden
                cache.set('maintenance_mode_status', maintenance_active, 60)
            except:
                pass
    
    return {
        'maintenance_mode': maintenance_active,
        'is_superuser': request.user.is_authenticated and request.user.is_superuser,
    }
