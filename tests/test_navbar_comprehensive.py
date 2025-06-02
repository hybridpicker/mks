"""
Umfassende Django Test Suite für MKS Navbar
Testet alle Funktionen: URLs, Design, Mobile, Desktop, Authentication
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponse
import re

User = get_user_model()  # Verwendet automatisch CustomUser


class NavbarTestCase(TestCase):
    """Base Test Case für Navbar Tests"""
    
    def setUp(self):
        """Setup für alle Tests"""
        self.client = Client()
        
        # Test User erstellen
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        # Staff User erstellen
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass123',
            email='staff@example.com',
            first_name='Staff',
            last_name='User',
            is_staff=True
        )
        
        # Superuser erstellen
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass123',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )

    def get_navbar_html(self, user=None):
        """Helper: Navbar HTML für User-Typ generieren"""
        if user:
            self.client.force_login(user)
            response = self.client.get('/')
        else:
            response = self.client.get('/')
        
        return response.content.decode('utf-8')


class NavbarUrlTests(NavbarTestCase):
    """Tests für Navbar URLs - das ursprüngliche Problem"""
    
    def test_orgelunterricht_url_not_hardcoded(self):
        """Test dass Orgelunterricht URL nicht hardkodiert ist"""
        html = self.get_navbar_html()
        self.assertNotIn('href="/orgelunterricht"', html,
                        "Hardkodierte Orgelunterricht URL gefunden!")
        
    def test_midi_band_url_not_hardcoded(self):
        """Test dass MIDI Band URL nicht hardkodiert ist"""
        html = self.get_navbar_html()
        self.assertNotIn('href="/midi-band"', html,
                        "Hardkodierte MIDI Band URL gefunden!")
        
    def test_orgelunterricht_url_resolves(self):
        """Test dass Orgelunterricht URL korrekt auflöst"""
        url = reverse('orgelunterricht')
        self.assertEqual(url, '/orgelunterricht/')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_midi_band_url_resolves(self):
        """Test dass MIDI Band URL korrekt auflöst"""
        url = reverse('midi_band')
        self.assertEqual(url, '/midi-band/')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_all_navbar_urls_resolve(self):
        """Test dass alle Navbar URLs korrekt auflösen"""
        urls_to_test = [
            'home_view',
            'teaching:teaching_music',
            'teaching:teaching_art', 
            'gallery_view',
            'teaching:all_teachers',
            'history',
            'blog_summary',
            'contact_email',
            'orgelunterricht',  # Das ursprüngliche Problem!
            'midi_band'         # Das ursprüngliche Problem!
        ]
        
        for url_name in urls_to_test:
            with self.subTest(url_name=url_name):
                try:
                    url = reverse(url_name)
                    response = self.client.get(url)
                    self.assertIn(response.status_code, [200, 302, 301],
                                f"URL {url_name} gab Status {response.status_code}")
                except Exception as e:
                    self.fail(f"URL {url_name} konnte nicht aufgelöst werden: {e}")


class NavbarAuthenticationTests(NavbarTestCase):
    """Tests für verschiedene Authentifizierungs-States"""
    
    def test_public_navbar_for_anonymous_user(self):
        """Test dass anonyme Benutzer die öffentliche Navbar sehen"""
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        
        # Public navbar sollte geladen werden
        template_names = [t.name for t in response.templates if hasattr(t, 'name')]
        self.assertIn('templates/navbar.html', template_names,
                     "Öffentliche Navbar wird nicht geladen!")
        
        # Admin-spezifische Elemente sollten NICHT vorhanden sein
        admin_elements = ['Blog verwalten', 'FAQ bearbeiten', 'Schüler:innen verwalten']
        for element in admin_elements:
            self.assertNotIn(element, html, f"Admin-Element '{element}' in öffentlicher Navbar!")
        
    def test_user_navbar_for_authenticated_user(self):
        """Test dass eingeloggte Benutzer die User-Navbar sehen"""
        self.client.force_login(self.test_user)
        response = self.client.get('/')
        
        # User navbar sollte geladen werden
        template_names = [t.name for t in response.templates if hasattr(t, 'name')]
        self.assertIn('templates/user_navbar.html', template_names,
                     "User-Navbar wird nicht geladen!")
        
    def test_admin_navbar_for_staff_user(self):
        """Test dass Staff-Benutzer Admin-Funktionen sehen"""
        self.client.force_login(self.staff_user)
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        
        # Admin-spezifische Links sollten vorhanden sein
        admin_content_found = ('Blog verwalten' in html or 
                             'FAQ bearbeiten' in html or
                             'Schüler:innen verwalten' in html or
                             'Veranstaltungen' in html)
        self.assertTrue(admin_content_found, "Keine Admin-Inhalte für Staff-User gefunden!")

    def test_navbar_user_context(self):
        """Test dass Navbar korrekte User-Informationen anzeigt"""
        self.client.force_login(self.test_user)
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        
        # Username oder Name sollte in der Navbar erscheinen
        user_indicators = [self.test_user.username, self.test_user.first_name]
        found_user_info = any(indicator in html for indicator in user_indicators if indicator)
        self.assertTrue(found_user_info, "Keine User-Informationen in Navbar gefunden!")


class NavbarStructureTests(NavbarTestCase):
    """Tests für die HTML-Struktur der Navbar"""
    
    def test_navbar_html_structure(self):
        """Test der grundlegenden HTML-Struktur"""
        html = self.get_navbar_html()
        
        # Header element sollte vorhanden sein
        self.assertIn('<header>', html, "Kein <header> Element gefunden!")
        
        # Navigation CSS-Klassen sollten vorhanden sein
        nav_indicators = ['nvb', 'dropdown', 'nav', 'bnbs']
        found_nav = any(indicator in html for indicator in nav_indicators)
        self.assertTrue(found_nav, "Keine Navigation-Indikatoren gefunden!")
        
    def test_navbar_main_navigation_items(self):
        """Test dass alle Haupt-Navigationspunkte vorhanden sind"""
        html = self.get_navbar_html()
        
        # Wichtige Navigation-Items
        required_nav_items = [
            'Musikschule',
            'Kunstschule', 
            'Galerie',
            'Über uns',
            'Kontakt'
        ]
        
        for item in required_nav_items:
            with self.subTest(nav_item=item):
                self.assertIn(item, html, f"Navigation item '{item}' fehlt!")

    def test_navbar_dropdown_content(self):
        """Test der Dropdown-Inhalte"""
        html = self.get_navbar_html()
        
        # Musikschule dropdown sollte Fachgruppen enthalten
        musikschule_items = [
            'Blasinstrumente',
            'Streichinstrumente', 
            'Tasteninstrumente',
            'Elementare Musikerziehung'
        ]
        
        for item in musikschule_items:
            self.assertIn(item, html, f"Musikschule item '{item}' fehlt!")
        
        # Orgelunterricht und MIDI Band sollten vorhanden sein
        self.assertIn('Orgelunterricht', html, "Orgelunterricht fehlt in Navigation!")
        self.assertIn('MIDI Band', html, "MIDI Band fehlt in Navigation!")

    def test_navbar_logo_present(self):
        """Test dass das Logo vorhanden ist"""
        html = self.get_navbar_html()
        
        # Logo-Indikatoren suchen
        logo_indicators = ['logo', 'svg', 'icon', 'home_view']
        found_logo = any(indicator in html.lower() for indicator in logo_indicators)
        self.assertTrue(found_logo, "Kein Logo in der Navbar gefunden!")


class NavbarMobileTests(NavbarTestCase):
    """Tests für Mobile Navigation"""
    
    def test_mobile_navigation_structure(self):
        """Test der mobilen Navigation-Struktur"""
        html = self.get_navbar_html()
        
        # Mobile navigation indicators
        mobile_indicators = [
            'mobile',
            'overlay',
            'mks-nav-mobile',
            'menuIcon',
            'hamburger'
        ]
        
        found_mobile = any(indicator in html for indicator in mobile_indicators)
        self.assertTrue(found_mobile, "Keine Mobile Navigation-Indikatoren gefunden!")
        
    def test_mobile_menu_content(self):
        """Test dass mobile Menü wichtige Links enthält"""
        html = self.get_navbar_html()
        
        # Wichtige Links sollten auch in mobile version sein
        mobile_nav_items = [
            'Musikschule',
            'Kunstschule',
            'Galerie', 
            'Orgelunterricht',
            'MIDI Band'
        ]
        
        for item in mobile_nav_items:
            with self.subTest(mobile_item=item):
                # Item sollte mindestens einmal vorkommen (Desktop oder Mobile)
                self.assertIn(item, html, f"Mobile item '{item}' fehlt!")

    def test_mobile_responsive_indicators(self):
        """Test dass responsive Design-Indikatoren vorhanden sind"""
        html = self.get_navbar_html()
        
        # CSS oder HTML-Indikatoren für responsive design
        responsive_indicators = [
            '@media',           # CSS media queries
            'mobile',          # Mobile CSS classes
            'overlay',         # Mobile overlay menu
            'dropdown',        # Responsive dropdowns
            'max-width'        # Responsive CSS
        ]
        
        found_responsive = any(indicator in html for indicator in responsive_indicators)
        self.assertTrue(found_responsive, "Keine Responsive Design-Indikatoren gefunden!")


class NavbarPerformanceTests(NavbarTestCase):
    """Performance Tests"""
    
    def test_navbar_load_time(self):
        """Test dass Navbar schnell lädt"""
        import time
        
        start_time = time.time()
        response = self.client.get('/')
        end_time = time.time()
        
        load_time = end_time - start_time
        
        # Navbar sollte unter 3 Sekunden laden (großzügig für Tests)
        self.assertLess(load_time, 3.0, f"Navbar load time zu hoch: {load_time:.2f}s")
        
    def test_navbar_html_size(self):
        """Test dass Navbar HTML nicht zu groß ist"""
        html = self.get_navbar_html()
        
        # Navbar HTML sollte unter 200KB sein (großzügig)
        html_size = len(html.encode('utf-8'))
        self.assertLess(html_size, 200000, f"Navbar HTML zu groß: {html_size} bytes")

    def test_no_excessive_duplicate_links(self):
        """Test dass nicht zu viele doppelte Links vorhanden sind"""
        html = self.get_navbar_html()
        
        # Orgelunterricht sollte nicht mehr als 8x vorkommen
        # (Desktop + Mobile + User navbar + evtl. mehrfach)
        orgelunterricht_count = html.count('Orgelunterricht')
        self.assertLessEqual(orgelunterricht_count, 8, 
                           f"Zu viele Orgelunterricht Links: {orgelunterricht_count}")
        
        # MIDI Band sollte auch nicht zu oft vorkommen
        midi_count = html.count('MIDI Band')
        self.assertLessEqual(midi_count, 8,
                           f"Zu viele MIDI Band Links: {midi_count}")


class NavbarTemplateTests(NavbarTestCase):
    """Tests für Template-Integration"""
    
    def test_navbar_template_inheritance(self):
        """Test dass Navbar korrekt in base.html eingebunden ist"""
        response = self.client.get('/')
        
        # base.html sollte verwendet werden
        template_names = [t.name for t in response.templates if hasattr(t, 'name')]
        self.assertIn('templates/base.html', template_names,
                     "base.html wird nicht verwendet!")
        
    def test_conditional_navbar_loading(self):
        """Test dass conditional navbar loading funktioniert"""
        # Anonymous user - navbar.html
        response = self.client.get('/')
        template_names = [t.name for t in response.templates if hasattr(t, 'name')]
        self.assertIn('templates/navbar.html', template_names,
                     "navbar.html wird für anonyme User nicht geladen!")
        
        # Authenticated user - user_navbar.html  
        self.client.force_login(self.test_user)
        response = self.client.get('/')
        template_names = [t.name for t in response.templates if hasattr(t, 'name')]
        self.assertIn('templates/user_navbar.html', template_names,
                     "user_navbar.html wird für eingeloggte User nicht geladen!")

    def test_navbar_context_variables(self):
        """Test dass Navbar Zugriff auf nötige Context-Variablen hat"""
        self.client.force_login(self.test_user)
        response = self.client.get('/')
        
        # Context sollte user haben
        self.assertIn('user', response.context, "User-Variable fehlt im Context!")
        self.assertEqual(response.context['user'], self.test_user)
        
        # Request sollte auch verfügbar sein
        self.assertIn('request', response.context, "Request-Variable fehlt im Context!")


class NavbarRegressionTests(NavbarTestCase):
    """Regression Tests - stellt sicher dass das ursprüngliche Problem gelöst ist"""
    
    def test_production_server_url_compatibility(self):
        """Test dass URLs production-server kompatibel sind"""
        html = self.get_navbar_html()
        
        # KEINE hardkodierten URLs
        hardcoded_urls = [
            'href="/orgelunterricht"',
            'href="/midi-band"'
        ]
        
        for hardcoded_url in hardcoded_urls:
            self.assertNotIn(hardcoded_url, html, 
                           f"KRITISCH: Hardkodierte URL gefunden: {hardcoded_url}")
    
    def test_django_url_tags_used(self):
        """Test dass Django URL tags verwendet werden (im Template-Source)"""
        import os
        
        templates_to_check = [
            '/Users/lukasschonsgibl/Coding/Django/mks/templates/templates/navbar.html',
            '/Users/lukasschonsgibl/Coding/Django/mks/templates/templates/user_navbar.html'
        ]
        
        for template_path in templates_to_check:
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    template_content = f.read()
                
                # Sollte Django URL tags haben (wenn Orgelunterricht erwähnt wird)
                if 'orgelunterricht' in template_content.lower():
                    self.assertIn("{% url 'orgelunterricht' %}", template_content,
                                f"Django URL tag fehlt in {os.path.basename(template_path)}")
    
    def test_original_design_preserved(self):
        """Test dass das ursprüngliche Design erhalten ist"""
        html = self.get_navbar_html()
        
        # Ursprüngliche CSS-Klassen sollten noch vorhanden sein
        original_classes = [
            'nvb',           # Navbar
            'dropdown',      # Dropdown-Menüs
            'bnbs',         # Navbar structure
            'bls'           # Logo section
        ]
        
        found_classes = 0
        for css_class in original_classes:
            if css_class in html:
                found_classes += 1
        
        # Mindestens die Hälfte der ursprünglichen Klassen sollten noch da sein
        self.assertGreaterEqual(found_classes, len(original_classes) // 2,
                              "Zu viele ursprüngliche CSS-Klassen entfernt - Design verändert!")

    def test_navbar_functionality_preserved(self):
        """Test dass alle ursprünglichen Navbar-Funktionen erhalten sind"""
        html = self.get_navbar_html()
        
        # Wichtige Funktionen sollten noch da sein
        functional_elements = [
            'dropdown',      # Dropdown-Funktionalität
            'button',        # Interaktive Elemente
            'href=',         # Links funktionieren
            'Musikschule',   # Haupt-Navigation
            'Orgelunterricht' # Das reparierte Element
        ]
        
        for element in functional_elements:
            self.assertIn(element, html, f"Funktionales Element '{element}' fehlt!")


class NavbarAccessibilityTests(NavbarTestCase):
    """Tests für Barrierefreiheit der Navbar"""
    
    def test_navbar_has_focusable_elements(self):
        """Test dass Navbar focusierbare Elemente hat"""
        html = self.get_navbar_html()
        
        # Focusierbare Elemente
        focusable_indicators = [
            'href=',         # Links
            '<button',       # Buttons
            'tabindex=',     # Explizite Tab-Reihenfolge
            '<a '           # Anchor tags
        ]
        
        found_focusable = sum(1 for indicator in focusable_indicators if indicator in html)
        self.assertGreater(found_focusable, 2, "Zu wenige focusierbare Elemente in Navbar!")

    def test_navbar_semantic_structure(self):
        """Test dass Navbar semantische HTML-Struktur hat"""
        html = self.get_navbar_html()
        
        # Semantische Elemente
        semantic_elements = [
            '<header>',      # Semantic header
            '<nav>',         # Navigation element (optional)
            '<button>',      # Proper buttons
            'role=',         # ARIA roles (optional)
        ]
        
        found_semantic = sum(1 for element in semantic_elements if element in html)
        self.assertGreater(found_semantic, 1, "Navbar braucht mehr semantische Struktur!")


# Test Runner für Command Line
class NavbarTestSuite:
    """Test Suite Runner für Navbar Tests"""
    
    @staticmethod
    def run_all_tests():
        """Führe alle Navbar Tests aus"""
        from django.test.utils import get_runner
        from django.conf import settings
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=2)
        
        test_labels = ['tests.test_navbar_comprehensive']
        failures = test_runner.run_tests(test_labels)
        
        return failures == 0
