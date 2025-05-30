from django.shortcuts import render
from django.core.cache import cache
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class MaintenanceModeMiddleware:
    """
    Middleware die prüft ob Maintenance Mode aktiv ist
    und normale Benutzer auf die Wartungsseite umleitet
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ausnahmen für Admin-Bereich und statische Dateien
        if any([
            request.path.startswith('/admin/'),
            request.path.startswith('/static/'),
            request.path.startswith('/media/'),
            request.path == '/maintenance/',
        ]):
            # Diese Pfade sind immer zugänglich
            response = self.get_response(request)
            return response
        
        try:
            # Cache nutzen für bessere Performance
            maintenance_status = cache.get('maintenance_mode_status')
            
            if maintenance_status is None:
                # Versuche aus der Datenbank zu laden
                from .models import MaintenanceMode
                
                # Prüfe ob Tabelle existiert
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'maintenance_maintenancemode'
                        );
                    """)
                    table_exists = cursor.fetchone()[0]
                    
                if table_exists:
                    maintenance = MaintenanceMode.load()
                    maintenance_status = maintenance.is_active
                    cache.set('maintenance_mode_status', maintenance_status, 60)
                else:
                    # Tabelle existiert nicht, Maintenance Mode ist deaktiviert
                    maintenance_status = False
                    logger.warning("MaintenanceMode Tabelle existiert nicht. Führe 'python manage.py setup_maintenance' aus.")
            
            # Prüfe ob Maintenance Mode aktiv ist
            if maintenance_status:
                # Prüfe ob User Superuser ist
                if not (request.user.is_authenticated and request.user.is_superuser):
                    # Zeige Maintenance Page
                    from .models import MaintenanceMode
                    maintenance = MaintenanceMode.load()
                    context = {
                        'maintenance': maintenance,
                        'hide_navbar': True,
                        'hide_footer': True,
                    }
                    return render(request, 'maintenance/under_construction.html', context)
                    
        except Exception as e:
            # Bei jedem Fehler, lass die Seite normal laden
            logger.error(f"Fehler in MaintenanceModeMiddleware: {str(e)}")
            pass
        
        response = self.get_response(request)
        return response