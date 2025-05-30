from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Erstellt die MaintenanceMode Tabelle direkt in der Datenbank'

    def handle(self, *args, **options):
        sql_file = os.path.join(os.path.dirname(__file__), '../../create_table.sql')
        
        try:
            with connection.cursor() as cursor:
                # Prüfe ob Tabelle bereits existiert
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'maintenance_maintenancemode'
                    );
                """)
                exists = cursor.fetchone()[0]
                
                if exists:
                    self.stdout.write(self.style.WARNING('Tabelle maintenance_maintenancemode existiert bereits'))
                else:
                    # Erstelle Tabelle
                    cursor.execute("""
                        CREATE TABLE maintenance_maintenancemode (
                            id SERIAL PRIMARY KEY,
                            is_active BOOLEAN NOT NULL DEFAULT FALSE,
                            title VARCHAR(200) NOT NULL DEFAULT 'Wartungsarbeiten',
                            message TEXT NOT NULL DEFAULT 'Wir führen gerade ein Update durch und sind bald wieder für Sie da!',
                            expected_downtime VARCHAR(100),
                            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    self.stdout.write(self.style.SUCCESS('Tabelle maintenance_maintenancemode wurde erstellt'))
                
                # Markiere Migration als angewendet
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('maintenance', '0001_initial', CURRENT_TIMESTAMP)
                    ON CONFLICT DO NOTHING;
                """)
                
                self.stdout.write(self.style.SUCCESS('Setup abgeschlossen!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler: {str(e)}'))