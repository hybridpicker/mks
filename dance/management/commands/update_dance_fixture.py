from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Aktualisiert die dance_fixture.json-Datei mit den aktuellen Daten aus der Datenbank'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='dance_fixture.json',
            help='Ausgabedatei (Standard: dance_fixture.json)',
        )

    def handle(self, *args, **options):
        output_file = options['output']
        output_path = os.path.join(settings.BASE_DIR, output_file)
        
        self.stdout.write(self.style.WARNING(f'Exportiere aktuelle Tanzdaten nach {output_path}...'))
        
        try:
            # Exportiere die Daten aus der Datenbank
            call_command(
                'dumpdata', 
                'dance.Teacher', 
                'dance.Course', 
                'dance.TimeSlot',
                '--indent=4',
                '--output=' + output_path
            )
            
            self.stdout.write(self.style.SUCCESS(f'Tanzdaten erfolgreich nach {output_path} exportiert!'))
            
            # Prüfe, ob die Datei erstellt wurde
            if os.path.exists(output_path):
                filesize = os.path.getsize(output_path)
                self.stdout.write(self.style.SUCCESS(f'Datei erstellt: {output_path} ({filesize} Bytes)'))
            else:
                self.stdout.write(self.style.ERROR(f'Datei wurde nicht erstellt: {output_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Fehler beim Exportieren der Daten: {str(e)}'))
