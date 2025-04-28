from django.core.management.base import BaseCommand
from dance.models import TimeSlot

class Command(BaseCommand):
    help = 'Bereinigt doppelte Standorte in der Datenbank'

    def handle(self, *args, **options):
        # Hole alle Standorte
        locations = TimeSlot.objects.values_list('location', flat=True).distinct()
        self.stdout.write(f"Gefundene Standorte: {len(locations)}")
        
        # Zeige alle Standorte an
        self.stdout.write("Gefundene Standorte:")
        for loc in sorted([l for l in locations if l]):
            count = TimeSlot.objects.filter(location=loc).count()
            self.stdout.write(f"  - {loc}: {count} Zeitfenster")
        
        # Normalisiere die Standortnamen
        standardize_map = {
            'campus': 'Campus',
            'Kampus': 'Campus',
            'CAMPUS': 'Campus',
            'kulturhaus wagram': 'Kulturhaus Wagram',
            'Kulturhaus-Wagram': 'Kulturhaus Wagram',
            'Wagram': 'Kulturhaus Wagram',
            'kulturhaus spratzern': 'Kulturhaus Spratzern',
            'Kulturhaus-Spratzern': 'Kulturhaus Spratzern',
            'Spratzern': 'Kulturhaus Spratzern',
        }
        
        updated_count = 0
        for old_name, new_name in standardize_map.items():
            count = TimeSlot.objects.filter(location=old_name).update(location=new_name)
            if count > 0:
                self.stdout.write(f"Aktualisiert: {count} Zeitfenster von '{old_name}' zu '{new_name}'")
                updated_count += count
        
        if updated_count == 0:
            self.stdout.write(self.style.SUCCESS("Keine Standorte benötigten Aktualisierung."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Insgesamt {updated_count} Zeitfenster aktualisiert."))
        
        # Zeige die aktualisierten Standorte an
        locations = TimeSlot.objects.values_list('location', flat=True).distinct()
        unique_locations = sorted([l for l in set(locations) if l])
        
        self.stdout.write("\nAktualisierte Standorte:")
        for loc in unique_locations:
            count = TimeSlot.objects.filter(location=loc).count()
            self.stdout.write(f"  - {loc}: {count} Zeitfenster")
