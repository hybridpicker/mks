from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from maintenance.models import MaintenanceMode
import os

User = get_user_model()


class MaintenanceModeTestCase(TestCase):
    """Tests für den Wartungsmodus"""
    
    def setUp(self):
        """Setup für jeden Test"""
        # Cache leeren
        cache.clear()
        
        # Maintenance Mode zurücksetzen
        os.environ.pop('MAINTENANCE_MODE', None)
        
        # Test Users erstellen
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='userpass123'
        )
        
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='staffpass123',
            is_staff=True
        )
        
        # Clients erstellen
        self.anonymous_client = Client()
        self.user_client = Client()
        self.staff_client = Client()
        self.superuser_client = Client()
        self.bot_client = Client()
        
        # Clients einloggen
        self.user_client.login(username='user', password='userpass123')
        self.staff_client.login(username='staff', password='staffpass123')
        self.superuser_client.login(username='admin', password='adminpass123')
        
        # Bot User-Agent setzen
        self.bot_client.defaults['HTTP_USER_AGENT'] = 'Googlebot/2.1 (+http://www.google.com/bot.html)'
        
    def tearDown(self):
        """Cleanup nach jedem Test"""
        cache.clear()
        os.environ.pop('MAINTENANCE_MODE', None)
        
    def activate_maintenance_mode(self):
        """Hilfsfunktion um Maintenance Mode zu aktivieren"""
        maintenance = MaintenanceMode.load()
        maintenance.is_active = True
        maintenance.title = "Wartungsarbeiten"
        maintenance.message = "Die Seite wird gerade gewartet."
        maintenance.save()
        
    def test_maintenance_mode_blocks_anonymous_users(self):
        """Test dass anonyme Benutzer blockiert werden"""
        self.activate_maintenance_mode()
        
        response = self.anonymous_client.get('/')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Wartungsarbeiten', response.content.decode())
        
    def test_maintenance_mode_blocks_normal_users(self):
        """Test dass normale eingeloggte Benutzer blockiert werden"""
        self.activate_maintenance_mode()
        
        response = self.user_client.get('/')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Wartungsarbeiten', response.content.decode())
        
    def test_maintenance_mode_blocks_staff_users(self):
        """Test dass Staff-Benutzer blockiert werden"""
        self.activate_maintenance_mode()
        
        response = self.staff_client.get('/')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Wartungsarbeiten', response.content.decode())
        
    def test_maintenance_mode_allows_superusers(self):
        """Test dass Superuser Zugriff haben"""
        self.activate_maintenance_mode()
        
        response = self.superuser_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Wartungsarbeiten', response.content.decode())
        
    def test_maintenance_mode_blocks_bots(self):
        """Test dass Bots blockiert werden"""
        self.activate_maintenance_mode()
        
        # Verschiedene Bot User-Agents testen
        bot_user_agents = [
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
            'facebookexternalhit/1.1',
            'Twitterbot/1.0',
            'WhatsApp/2.19.81',
            'LinkedInBot/1.0',
            'Slackbot-LinkExpanding 1.0',
        ]
        
        for user_agent in bot_user_agents:
            client = Client()
            client.defaults['HTTP_USER_AGENT'] = user_agent
            response = client.get('/')
            self.assertEqual(
                response.status_code, 503,
                f"Bot mit User-Agent '{user_agent}' sollte blockiert werden"
            )
            self.assertIn('Wartungsarbeiten', response.content.decode())
            
    @override_settings(DEBUG=True)
    def test_maintenance_mode_with_debug_true_blocks_anonymous(self):
        """Test dass auch mit DEBUG=True anonyme Benutzer blockiert werden"""
        self.activate_maintenance_mode()
        
        response = self.anonymous_client.get('/')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Wartungsarbeiten', response.content.decode())
        
    @override_settings(DEBUG=True)
    def test_maintenance_mode_with_debug_true_blocks_normal_users(self):
        """Test dass auch mit DEBUG=True normale Benutzer blockiert werden"""
        self.activate_maintenance_mode()
        
        response = self.user_client.get('/')
        self.assertEqual(response.status_code, 503)
        self.assertIn('Wartungsarbeiten', response.content.decode())
        
    @override_settings(DEBUG=True)
    def test_maintenance_mode_with_debug_true_allows_superusers(self):
        """Test dass auch mit DEBUG=True Superuser Zugriff haben"""
        self.activate_maintenance_mode()
        
        response = self.superuser_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Wartungsarbeiten', response.content.decode())
        
    @override_settings(DEBUG=False)
    def test_maintenance_mode_with_debug_false_blocks_all_except_superuser(self):
        """Test dass mit DEBUG=False alle außer Superuser blockiert werden"""
        self.activate_maintenance_mode()
        
        # Anonyme Benutzer
        response = self.anonymous_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        # Normale Benutzer
        response = self.user_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        # Staff Benutzer
        response = self.staff_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        # Bots
        response = self.bot_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        # Nur Superuser haben Zugriff
        response = self.superuser_client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_maintenance_mode_exempt_paths(self):
        """Test dass bestimmte Pfade immer erreichbar sind"""
        self.activate_maintenance_mode()
        
        exempt_paths = [
            '/admin/',
            '/static/test.css',
            '/media/test.jpg',
            '/maintenance/',
        ]
        
        for path in exempt_paths:
            response = self.anonymous_client.get(path, follow=False)
            # Diese Pfade sollten nicht 503 zurückgeben
            self.assertNotEqual(
                response.status_code, 503,
                f"Pfad {path} sollte nicht blockiert werden"
            )
            
    def test_maintenance_mode_via_environment_variable(self):
        """Test dass Maintenance Mode über Environment Variable funktioniert"""
        os.environ['MAINTENANCE_MODE'] = 'true'
        
        response = self.anonymous_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        response = self.superuser_client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_maintenance_mode_bypass_token(self):
        """Test dass Bypass Token funktioniert"""
        self.activate_maintenance_mode()
        
        # Ohne Token - blockiert
        response = self.anonymous_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        # Mit falschem Token - blockiert
        response = self.anonymous_client.get('/?bypass=wrong-token')
        self.assertEqual(response.status_code, 503)
        
        # Mit richtigem Token - Zugriff
        with self.settings(MAINTENANCE_BYPASS_TOKEN='secret-token'):
            response = self.anonymous_client.get('/?bypass=secret-token')
            self.assertEqual(response.status_code, 200)
            
            # Cookie wird gesetzt
            self.assertIn('maintenance_bypass', response.cookies)
            
            # Nachfolgende Requests funktionieren mit Cookie
            response = self.anonymous_client.get('/')
            self.assertEqual(response.status_code, 200)
            
    def test_maintenance_mode_crawler_detection(self):
        """Test dass verschiedene Crawler erkannt und blockiert werden"""
        self.activate_maintenance_mode()
        
        # Bekannte Crawler/Bot Patterns
        crawler_patterns = [
            'bot', 'crawler', 'spider', 'scraper',
            'facebookexternalhit', 'WhatsApp', 'Slack',
            'TwitterBot', 'LinkedInBot', 'Pinterest',
            'Googlebot', 'bingbot', 'Yandex', 'Baidu',
            'DuckDuckBot', 'Sogou', 'Exabot', 'ia_archiver',
            'curl', 'wget', 'python-requests', 'axios',
            'Go-http-client', 'Java/', 'Apache-HttpClient',
            'PostmanRuntime', 'insomnia'
        ]
        
        for pattern in crawler_patterns:
            client = Client()
            client.defaults['HTTP_USER_AGENT'] = f'Mozilla/5.0 {pattern}/1.0'
            response = client.get('/')
            self.assertEqual(
                response.status_code, 503,
                f"Crawler mit Pattern '{pattern}' sollte blockiert werden"
            )
            
    def test_maintenance_page_content(self):
        """Test dass die Maintenance Page die richtigen Inhalte zeigt"""
        maintenance = MaintenanceMode.load()
        maintenance.is_active = True
        maintenance.title = "Geplante Wartung"
        maintenance.message = "Wir aktualisieren unsere Server."
        maintenance.expected_downtime = "2 Stunden"
        maintenance.save()
        
        response = self.anonymous_client.get('/')
        self.assertEqual(response.status_code, 503)
        
        content = response.content.decode()
        self.assertIn('Geplante Wartung', content)
        self.assertIn('Wir aktualisieren unsere Server.', content)
        self.assertIn('2 Stunden', content)
        
    def test_maintenance_mode_ajax_requests(self):
        """Test dass AJAX Requests auch blockiert werden"""
        self.activate_maintenance_mode()
        
        # AJAX Request von normalem Benutzer
        response = self.user_client.get(
            '/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 503)
        
        # AJAX Request von Superuser
        response = self.superuser_client.get(
            '/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
    def test_maintenance_mode_post_requests(self):
        """Test dass POST Requests auch blockiert werden"""
        self.activate_maintenance_mode()
        
        # POST von normalem Benutzer
        response = self.user_client.post('/', {'test': 'data'})
        self.assertEqual(response.status_code, 503)
        
        # POST von Superuser
        response = self.superuser_client.post('/', {'test': 'data'})
        self.assertEqual(response.status_code, 200)
