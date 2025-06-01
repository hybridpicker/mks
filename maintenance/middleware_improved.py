from django.shortcuts import render
from django.core.cache import cache
from django.db import connection, OperationalError
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

class MaintenanceModeMiddleware:
    """
    Middleware die prüft ob Maintenance Mode aktiv ist
    und normale Benutzer auf die Wartungsseite umleitet
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Fallback auf Environment Variable für Deployment
        self.env_maintenance = os.environ.get('MAINTENANCE_MODE', 'false').lower() == 'true'

    def __call__(self, request):
        # Ausnahmen für Admin-Bereich und statische Dateien
        exempt_paths = [
            '/admin/',
            '/static/',
            '/media/',
            '/maintenance/',
            '/__debug__/',
            '/favicon.ico',
        ]
        
        # API Endpoints die während Maintenance erreichbar sein sollen
        if hasattr(settings, 'MAINTENANCE_EXEMPT_PATHS'):
            exempt_paths.extend(settings.MAINTENANCE_EXEMPT_PATHS)
        
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
        
        # Prüfe Maintenance Status
        is_maintenance = self._check_maintenance_status()
        
        if is_maintenance:
            # Prüfe ob User Superuser ist oder spezielles Maintenance-Bypass Token hat
            bypass_token = request.GET.get('bypass') or request.COOKIES.get('maintenance_bypass')
            correct_bypass = getattr(settings, 'MAINTENANCE_BYPASS_TOKEN', None)
            
            if bypass_token and correct_bypass and bypass_token == correct_bypass:
                response = self.get_response(request)
                response.set_cookie('maintenance_bypass', bypass_token, max_age=3600)
                return response
            
            if not (request.user.is_authenticated and request.user.is_superuser):
                # Zeige Maintenance Page
                return self._render_maintenance_page(request)
        
        return self.get_response(request)
    
    def _check_maintenance_status(self):
        """Prüft den Maintenance Status mit mehreren Fallbacks"""
        
        # 1. Priorität: Environment Variable (für schnelles Ein-/Ausschalten)
        if self.env_maintenance:
            return True
        
        # 2. Priorität: Settings Variable
        if hasattr(settings, 'MAINTENANCE_MODE') and settings.MAINTENANCE_MODE:
            return True
        
        # 3. Priorität: Cache
        maintenance_status = cache.get('maintenance_mode_status')
        if maintenance_status is not None:
            return maintenance_status
        
        # 4. Priorität: Datenbank (mit Fehlerbehandlung)
        try:
            from .models import MaintenanceMode
            
            # Prüfe ob Tabelle existiert
            with connection.cursor() as cursor:
                if connection.vendor == 'postgresql':
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'maintenance_maintenancemode'
                        );
                    """)
                elif connection.vendor == 'sqlite':
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name='maintenance_maintenancemode';
                    """)
                    result = cursor.fetchone()
                    table_exists = result is not None
                else:
                    # Andere Datenbanken
                    table_exists = True
                
                if connection.vendor == 'postgresql':
                    table_exists = cursor.fetchone()[0]
                
                if table_exists:
                    maintenance = MaintenanceMode.load()
                    maintenance_status = maintenance.is_active
                    # Cache für 60 Sekunden
                    cache.set('maintenance_mode_status', maintenance_status, 60)
                    return maintenance_status
                    
        except (OperationalError, Exception) as e:
            logger.warning(f"Konnte Maintenance Status nicht aus DB laden: {str(e)}")
            # Bei Datenbankfehlern auf Environment/Settings zurückfallen
            pass
        
        return False
    
    def _render_maintenance_page(self, request):
        """Rendert die Maintenance Seite mit Fallback-Werten"""
        context = {
            'maintenance': {
                'title': getattr(settings, 'MAINTENANCE_TITLE', 'Wartungsarbeiten'),
                'message': getattr(settings, 'MAINTENANCE_MESSAGE', 
                    'Wir führen gerade ein Update durch und sind bald wieder für Sie da!'),
                'expected_downtime': getattr(settings, 'MAINTENANCE_DOWNTIME', None)
            },
            'hide_navbar': True,
            'hide_footer': True,
        }
        
        # Versuche Daten aus DB zu laden
        try:
            from .models import MaintenanceMode
            maintenance = MaintenanceMode.load()
            context['maintenance'] = maintenance
        except:
            pass
        
        return render(request, 'maintenance/under_construction.html', context, status=503)
