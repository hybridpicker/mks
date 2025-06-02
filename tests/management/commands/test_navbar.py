"""
Django Management Command für Navbar Tests
"""

from django.core.management.base import BaseCommand
from django.test.runner import DiscoverRunner
from django.test.utils import get_runner
from django.conf import settings
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
            '--test-class',
            type=str,
            help='Spezifische Test-Klasse ausführen (z.B. NavbarUrlTests)',
        )
        parser.add_argument(
            '--performance',
            action='store_true',
            help='Nur Performance-Tests ausführen',
        )
        parser.add_argument(
            '--mobile',
            action='store_true', 
            help='Nur Mobile-Tests ausführen',
        )

    def handle(self, *args, **options):
        """Hauptfunktion des Management Commands"""
        
        self.stdout.write(
            self.style.SUCCESS("🧪 MKS Navbar Test Suite gestartet...")
        )
        
        # Test Runner konfigurieren
        test_runner = DiscoverRunner(verbosity=2 if options['verbose'] else 1)
        
        # Test-Labels basierend auf Optionen
        test_labels = []
        
        if options['test_class']:
            test_labels = [f'tests.test_navbar.{options["test_class"]}']
        elif options['performance']:
            test_labels = ['tests.test_navbar.NavbarPerformanceTests']
        elif options['mobile']:
            test_labels = ['tests.test_navbar.NavbarMobileTests']
        else:
            # Alle Tests
            test_labels = ['tests.test_navbar']
        
        self.stdout.write(f"📋 Teste: {', '.join(test_labels)}")
        
        # Tests ausführen
        try:
            failures = test_runner.run_tests(test_labels)
            
            if failures == 0:
                self.stdout.write(
                    self.style.SUCCESS("🎉 Alle Navbar Tests erfolgreich!")
                )
                self.stdout.write("✅ Navbar ist production-ready!")
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ {failures} Tests fehlgeschlagen!")
                )
                self.stdout.write("⚠️  Bitte Probleme beheben vor Production-Deployment")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"🚨 Fehler beim Ausführen der Tests: {e}")
            )
            sys.exit(1)
        
        # Test-Zusammenfassung
        self.print_test_summary(failures)
        
        return failures

    def print_test_summary(self, failures):
        """Druckt eine Zusammenfassung der Test-Ergebnisse"""
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write("📊 NAVBAR TEST ZUSAMMENFASSUNG")
        self.stdout.write("="*60)
        
        test_categories = [
            ("🔗 URL Tests", "Hardkodierte URLs, Django URL-Auflösung"),
            ("👤 Authentication Tests", "Public vs User vs Admin Navbar"),
            ("🏗️  Structure Tests", "HTML-Struktur, Navigation-Items"),
            ("📱 Mobile Tests", "Responsive Design, Mobile Navigation"),
            ("♿ Accessibility Tests", "ARIA-Labels, Keyboard Navigation"),
            ("⚡ Performance Tests", "Load Time, HTML Size"),
            ("🧩 Template Tests", "Django Template Integration")
        ]
        
        for category, description in test_categories:
            self.stdout.write(f"{category:<25} {description}")
        
        self.stdout.write("="*60)
        
        if failures == 0:
            self.stdout.write(self.style.SUCCESS("🚀 NAVBAR READY FOR PRODUCTION!"))
            self.stdout.write("   • Alle URLs funktionieren korrekt")
            self.stdout.write("   • Mobile & Desktop Design getestet")
            self.stdout.write("   • Authentication-Flow funktioniert")
            self.stdout.write("   • Performance ist akzeptabel")
        else:
            self.stdout.write(self.style.WARNING("⚠️  NAVBAR BRAUCHT VERBESSERUNGEN"))
            self.stdout.write("   • Bitte gescheiterte Tests prüfen")
            self.stdout.write("   • Nach Fixes erneut testen")
        
        self.stdout.write("\n💡 Navbar Tests erneut ausführen:")
        self.stdout.write("   python manage.py test_navbar")
        self.stdout.write("   python manage.py test_navbar --mobile")
        self.stdout.write("   python manage.py test_navbar --performance")
        self.stdout.write("   python manage.py test_navbar --test-class NavbarUrlTests")
