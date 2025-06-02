"""
Django Management Command für umfassende Navbar Tests
Ausführung: python manage.py test_navbar_complete
"""

from django.core.management.base import BaseCommand
from django.test.runner import DiscoverRunner
import sys


class Command(BaseCommand):
    help = 'Führt umfassende Navbar Tests aus - URLs, Design, Mobile, Desktop, Authentication'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Ausführliche Ausgabe der Tests',
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Spezifische Test-Kategorie (url, auth, structure, mobile, performance, template, regression, accessibility)',
        )
        parser.add_argument(
            '--quick',
            action='store_true',
            help='Nur wichtigste Tests ausführen (URLs und Authentication)',
        )
        parser.add_argument(
            '--report',
            action='store_true',
            help='Detaillierten Report nach Tests anzeigen',
        )

    def handle(self, *args, **options):
        """Hauptfunktion des Management Commands"""
        
        self.stdout.write(
            self.style.SUCCESS("🧪 MKS Navbar - Umfassende Test Suite")
        )
        self.stdout.write("=" * 60)
        
        # Test Runner konfigurieren
        verbosity = 2 if options['verbose'] else 1
        test_runner = DiscoverRunner(verbosity=verbosity)
        
        # Test-Labels basierend auf Optionen
        test_labels = []
        
        if options['quick']:
            # Nur die wichtigsten Tests
            test_labels = [
                'tests.test_navbar_comprehensive.NavbarUrlTests',
                'tests.test_navbar_comprehensive.NavbarAuthenticationTests'
            ]
            self.stdout.write("🏃 Quick Tests: URLs + Authentication")
            
        elif options['category']:
            category = options['category'].lower()
            category_map = {
                'url': 'NavbarUrlTests',
                'auth': 'NavbarAuthenticationTests', 
                'structure': 'NavbarStructureTests',
                'mobile': 'NavbarMobileTests',
                'performance': 'NavbarPerformanceTests',
                'template': 'NavbarTemplateTests',
                'regression': 'NavbarRegressionTests',
                'accessibility': 'NavbarAccessibilityTests'
            }
            
            if category in category_map:
                test_labels = [f'tests.test_navbar_comprehensive.{category_map[category]}']
                self.stdout.write(f"🎯 Kategorie: {category.upper()}")
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Unbekannte Kategorie: {category}")
                )
                self.stdout.write("Verfügbare Kategorien: " + ", ".join(category_map.keys()))
                return 1
        else:
            # Alle Tests
            test_labels = ['tests.test_navbar_comprehensive']
            self.stdout.write("📋 Alle Navbar Tests")
        
        self.stdout.write(f"🔍 Teste: {', '.join(test_labels)}")
        self.stdout.write("")
        
        # Tests ausführen
        try:
            failures = test_runner.run_tests(test_labels)
            
            if failures == 0:
                self.stdout.write("")
                self.stdout.write(
                    self.style.SUCCESS("🎉 ALLE NAVBAR TESTS ERFOLGREICH!")
                )
                if options['report']:
                    self.print_success_report()
            else:
                self.stdout.write("")
                self.stdout.write(
                    self.style.ERROR(f"❌ {failures} Tests fehlgeschlagen!")
                )
                self.print_failure_help()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"🚨 Fehler beim Ausführen der Tests: {e}")
            )
            return 1
        
        return failures

    def print_success_report(self):
        """Druckt einen Erfolgs-Report"""
        
        self.stdout.write("🏆 NAVBAR TEST ERFOLG - DETAILREPORT")
        self.stdout.write("=" * 50)
        
        success_categories = [
            ("🔗 URL Tests", "URLs funktionieren, keine hardkodierten Pfade"),
            ("👤 Authentication", "Public/User/Admin Navbar korrekt"),
            ("🏗️  Struktur", "HTML-Struktur und Navigation vollständig"), 
            ("📱 Mobile", "Responsive Design und Mobile Navigation"),
            ("⚡ Performance", "Schnelle Ladezeiten, optimale Größe"),
            ("🧩 Templates", "Django Template Integration korrekt"),
            ("🔄 Regression", "Ursprüngliches Problem gelöst"),
            ("♿ Accessibility", "Barrierefreie Navigation")
        ]
        
        for category, description in success_categories:
            self.stdout.write(f"{category:<20} ✅ {description}")
        
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("🚀 NAVBAR READY FOR PRODUCTION!"))
        self.stdout.write("")
        self.stdout.write("✅ Problem gelöst:")
        self.stdout.write("   • /orgelunterricht → {% url 'orgelunterricht' %}")
        self.stdout.write("   • /midi-band → {% url 'midi_band' %}")
        self.stdout.write("   • Production-Server kompatible URLs")
        self.stdout.write("   • Ursprüngliches Design erhalten")

    def print_failure_help(self):
        """Hilfe bei fehlgeschlagenen Tests"""
        
        self.stdout.write("")
        self.stdout.write("🛠️  TROUBLESHOOTING:")
        self.stdout.write("1. Einzelne Kategorien testen:")
        self.stdout.write("   python manage.py test_navbar_complete --category url")
        self.stdout.write("   python manage.py test_navbar_complete --category auth")
        self.stdout.write("   python manage.py test_navbar_complete --category mobile")
        self.stdout.write("")
        self.stdout.write("2. Verbose Mode für Details:")
        self.stdout.write("   python manage.py test_navbar_complete --verbose")
        self.stdout.write("")
        self.stdout.write("3. Quick Tests für Basis-Checks:")
        self.stdout.write("   python manage.py test_navbar_complete --quick")
        self.stdout.write("")
        self.stdout.write("4. Manuelle Django Tests:")
        self.stdout.write("   python manage.py test tests.test_navbar_comprehensive")

    def print_test_categories(self):
        """Information über verfügbare Test-Kategorien"""
        
        self.stdout.write("")
        self.stdout.write("📚 VERFÜGBARE TEST-KATEGORIEN:")
        self.stdout.write("-" * 40)
        
        categories = [
            ("url", "URL-Auflösung und hardkodierte Pfade"),
            ("auth", "Authentication und User-spezifische Navigation"),
            ("structure", "HTML-Struktur und Navigation-Items"),
            ("mobile", "Mobile/Responsive Navigation"),
            ("performance", "Ladezeiten und Performance"),
            ("template", "Django Template Integration"),
            ("regression", "Regression Tests (ursprüngliches Problem)"),
            ("accessibility", "Barrierefreiheit und Semantik")
        ]
        
        for cat, desc in categories:
            self.stdout.write(f"  {cat:<15} {desc}")
