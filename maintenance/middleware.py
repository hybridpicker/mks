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
    und normale Benutzer auf die Wartungsseite umleitet.
    
    WICHTIG: Im Wartungsmodus haben NUR Superuser Zugriff!
    - Keine Ausnahme für DEBUG=True
    - Keine Ausnahme für Staff-User
    - Keine Ausnahme für Bots
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
        
        # Prüfe ob der Pfad ausgenommen ist
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
        
        # Prüfe Maintenance Status
        is_maintenance = self._check_maintenance_status()
        
        if is_maintenance:
            # Bot Detection - Bots bekommen auch Maintenance Page
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            is_bot = self._is_bot(user_agent)
            
            if is_bot:
                logger.info(f"Bot blocked during maintenance: {user_agent}")
                return self._render_maintenance_page(request)
            
            # Prüfe ob User Superuser ist oder spezielles Maintenance-Bypass Token hat
            bypass_token = request.GET.get('bypass') or request.COOKIES.get('maintenance_bypass')
            correct_bypass = getattr(settings, 'MAINTENANCE_BYPASS_TOKEN', None)
            
            # Bypass Token Check
            if bypass_token and correct_bypass and bypass_token == correct_bypass:
                response = self.get_response(request)
                response.set_cookie('maintenance_bypass', bypass_token, max_age=3600)
                logger.info(f"Maintenance bypass used from IP: {self._get_client_ip(request)}")
                return response
            
            # WICHTIG: Nur Superuser haben Zugriff - keine anderen Ausnahmen!
            # Dies gilt auch für DEBUG=True und Staff-User
            if not (request.user.is_authenticated and request.user.is_superuser):
                logger.info(f"Access blocked during maintenance for: {request.user if request.user.is_authenticated else 'Anonymous'}")
                return self._render_maintenance_page(request)
            else:
                logger.info(f"Superuser {request.user.username} accessed site during maintenance")
        
        return self.get_response(request)
    
    def _is_bot(self, user_agent):
        """Erkennt Bots anhand des User-Agent"""
        bot_indicators = [
            'bot', 'crawler', 'spider', 'scraper', 'crawl',
            'slurp', 'mediapartners', 'adsbot', 'feedfetcher',
            'facebookexternalhit', 'whatsapp', 'slack',
            'twitterbot', 'linkedinbot', 'pinterest',
            'googlebot', 'bingbot', 'yandex', 'baidu',
            'duckduckbot', 'sogou', 'exabot', 'ia_archiver',
            'curl', 'wget', 'python-requests', 'axios',
            'go-http-client', 'java/', 'apache-httpclient',
            'postmanruntime', 'insomnia', 'paw/', 'httpie',
            'scrapy', 'nutch', 'phpcrawl', 'larbin',
            'libwww', 'lwp-trivial', 'httrack', 'harvest',
            'archiver', 'monitor', 'downloader', 'checker',
            'validator', 'fetcher', 'analyzer', 'extractor'
        ]
        
        return any(indicator in user_agent for indicator in bot_indicators)
    
    def _get_client_ip(self, request):
        """Ermittelt die Client IP-Adresse"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
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
                    table_exists = cursor.fetchone()[0]
                elif connection.vendor == 'sqlite':
                    cursor.execute("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name='maintenance_maintenancemode';
                    """)
                    result = cursor.fetchone()
                    table_exists = result is not None
                else:
                    # Andere Datenbanken - versuche es einfach
                    table_exists = True
                
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
        # Log maintenance page access
        ip = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        logger.info(f"Maintenance page shown to IP: {ip}, User-Agent: {user_agent}")
        
        context = {
            'maintenance': {
                'title': getattr(settings, 'MAINTENANCE_TITLE', 'Wartungsarbeiten'),
                'message': getattr(settings, 'MAINTENANCE_MESSAGE', 
                    'Wir führen gerade ein Update durch und sind bald wieder für Sie da!'),
                'expected_downtime': getattr(settings, 'MAINTENANCE_DOWNTIME', None)
            },
            'hide_navbar': True,
            'hide_footer': True,
            'is_maintenance': True,
        }
        
        # Versuche Daten aus DB zu laden
        try:
            from .models import MaintenanceMode
            maintenance = MaintenanceMode.load()
            context['maintenance'] = maintenance
        except:
            pass
        
        # Wichtig: HTTP Status 503 (Service Unavailable)
        return render(request, 'maintenance/under_construction.html', context, status=503)
