from django.core.management.base import BaseCommand
from django.db import connection
import os
import sys
from pathlib import Path
from django.conf import settings
import time

class Command(BaseCommand):
    help = 'Fügt die location-Spalte zur dance_timeslot-Tabelle hinzu (mit SQL-Fallback)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-sql',
            action='store_true',
            help='Verwendet SQL-Befehle anstelle von Django-Migrationen',
        )

    def handle(self, *args, **options):
        force_sql = options['force_sql']
        
        self.stdout.write(self.style.WARNING('Überprüfe Datenbank-Verbindung...'))
        db_engine = connection.vendor
        self.stdout.write(f"Datenbank-Engine: {db_engine}")
        
        # Überprüfe, ob die Spalte bereits existiert
        column_exists = self.check_column_exists('dance_timeslot', 'location')
        
        if column_exists:
            self.stdout.write(self.style.SUCCESS('Die Spalte "location" existiert bereits in der Tabelle "dance_timeslot".'))
            return
        
        # Versuche, die Migration mit Django-Migrationen zu erstellen und anzuwenden
        if not force_sql:
            try:
                self.stdout.write(self.style.WARNING('Erstelle eine neue Migration für die location-Spalte...'))
                
                # Überprüfe, ob die Migrationsdatei bereits existiert
                migration_file = self.find_migration_file('0002_timeslot_location.py')
                
                if migration_file:
                    self.stdout.write(f"Migration existiert bereits: {migration_file}")
                else:
                    # Erstelle eine neue Migrationsdatei
                    self.create_migration_file()
                
                # Wende die Migration an
                self.stdout.write(self.style.WARNING('Wende die Migration an...'))
                self.apply_migration()
                
                # Überprüfe erneut, ob die Spalte existiert
                column_exists = self.check_column_exists('dance_timeslot', 'location')
                
                if column_exists:
                    self.stdout.write(self.style.SUCCESS('Migration erfolgreich angewendet!'))
                    return
                else:
                    self.stdout.write(self.style.ERROR('Migration konnte nicht angewendet werden. Versuche SQL-Fallback...'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Fehler bei der Migration: {str(e)}'))
                self.stdout.write(self.style.WARNING('Versuche SQL-Fallback...'))
        
        # SQL-Fallback
        self.stdout.write(self.style.WARNING('Verwende direktes SQL, um die Spalte hinzuzufügen...'))
        
        try:
            self.add_column_with_sql()
            
            # Überprüfe erneut, ob die Spalte existiert
            column_exists = self.check_column_exists('dance_timeslot', 'location')
            
            if column_exists:
                self.stdout.write(self.style.SUCCESS('SQL-Befehl erfolgreich ausgeführt!'))
            else:
                self.stdout.write(self.style.ERROR('Spalte konnte nicht hinzugefügt werden. Bitte überprüfen Sie die Datenbank manuell.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler beim Ausführen des SQL-Befehls: {str(e)}'))
    
    def check_column_exists(self, table_name, column_name):
        """Überprüft, ob die Spalte in der Tabelle existiert."""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.columns "
                    "WHERE table_name = %s AND column_name = %s AND table_schema = DATABASE()",
                    [table_name, column_name]
                )
            elif connection.vendor == 'postgresql':
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.columns "
                    "WHERE table_name = %s AND column_name = %s",
                    [table_name, column_name]
                )
            elif connection.vendor == 'sqlite':
                cursor.execute(
                    "PRAGMA table_info(%s)" % table_name
                )
                return any(column[1] == column_name for column in cursor.fetchall())
            else:
                self.stdout.write(self.style.ERROR(f'Nicht unterstütztes Datenbank-System: {connection.vendor}'))
                return False
            
            result = cursor.fetchone()[0]
            return result > 0
    
    def find_migration_file(self, filename):
        """Sucht nach einer bestimmten Migrationsdatei."""
        migrations_dir = os.path.join(settings.BASE_DIR, 'dance', 'migrations')
        for root, dirs, files in os.walk(migrations_dir):
            if filename in files:
                return os.path.join(root, filename)
        return None
    
    def create_migration_file(self):
        """Erstellt eine neue Migrationsdatei für die location-Spalte."""
        migrations_dir = os.path.join(settings.BASE_DIR, 'dance', 'migrations')
        migration_file = os.path.join(migrations_dir, '0002_timeslot_location.py')
        
        # Nur erstellen, wenn die Datei nicht existiert
        if not os.path.exists(migration_file):
            # Stelle sicher, dass das Verzeichnis existiert
            os.makedirs(migrations_dir, exist_ok=True)
            
            # Stelle sicher, dass __init__.py existiert
            init_file = os.path.join(migrations_dir, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    pass
            
            # Erstelle die Migrationsdatei
            with open(migration_file, 'w', encoding='utf-8') as f:
                f.write("""from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='location',
            field=models.CharField(blank=True, help_text='Optional, z.B. Campus oder Kulturheim Spratzern', max_length=100, null=True, verbose_name='Standort'),
        ),
    ]
""")
            
            self.stdout.write(self.style.SUCCESS(f'Migrationsdatei erstellt: {migration_file}'))
        else:
            self.stdout.write(f'Migrationsdatei existiert bereits: {migration_file}')
    
    def apply_migration(self):
        """Wendet die Migration an."""
        from django.core.management import call_command
        call_command('migrate', 'dance', '0002_timeslot_location')
    
    def add_column_with_sql(self):
        """Fügt die Spalte mit SQL hinzu."""
        with connection.cursor() as cursor:
            if connection.vendor == 'mysql':
                cursor.execute(
                    "ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100) NULL"
                )
            elif connection.vendor == 'postgresql':
                cursor.execute(
                    "ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100) NULL"
                )
            elif connection.vendor == 'sqlite':
                cursor.execute(
                    "ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100)"
                )
            else:
                raise ValueError(f'Nicht unterstütztes Datenbank-System: {connection.vendor}')

if __name__ == '__main__':
    # Ermöglicht das Ausführen als Standalone-Script
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'fix_timeslot_location'])
