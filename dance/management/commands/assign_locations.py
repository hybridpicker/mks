from django.core.management.base import BaseCommand
from dance.models import Teacher, TimeSlot

class Command(BaseCommand):
    help = 'Weist Standorte zu den Zeitfenstern basierend auf den Lehrern zu'

    def handle(self, *args, **options):
        # Definiere die Lehrer-zu-Standort-Zuordnung
        teacher_location_map = {
            'Marijana Zeisel': 'Campus',
            'Yulia Bauer': 'Campus',
            'Chulpan Usmanova': 'Kulturhaus Wagram',
            'Anna Grüssinger': 'Kulturhaus Spratzern',
            'Katharina Holzweber': 'Kulturhaus Spratzern',
        }
        
        # Aktualisierungsstatistiken
        updated_count = 0
        skipped_count = 0
        
        # Laufe durch alle Lehrer
        for teacher_name, location in teacher_location_map.items():
            self.stdout.write(f"Suche Zeitfenster für Lehrer: {teacher_name}")
            
            # Finde den Lehrer anhand des Namens
            try:
                teachers = Teacher.objects.filter(name__icontains=teacher_name)
                
                if not teachers.exists():
                    self.stdout.write(self.style.WARNING(f"Lehrer '{teacher_name}' nicht gefunden."))
                    continue
                
                # Da icontains verwendet wird, könnte es mehrere Übereinstimmungen geben
                for teacher in teachers:
                    # Hole alle Zeitfenster für die Kurse dieses Lehrers
                    timeslots = TimeSlot.objects.filter(course__teacher=teacher)
                    
                    if not timeslots.exists():
                        self.stdout.write(self.style.WARNING(f"Keine Zeitfenster für Lehrer '{teacher.name}' gefunden."))
                        continue
                    
                    # Aktualisiere den Standort für jedes Zeitfenster
                    for timeslot in timeslots:
                        timeslot.location = location
                        timeslot.save()
                        updated_count += 1
                    
                    self.stdout.write(self.style.SUCCESS(
                        f"Standort '{location}' für {timeslots.count()} Zeitfenster von '{teacher.name}' aktualisiert."
                    ))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Fehler bei Lehrer '{teacher_name}': {str(e)}"))
                skipped_count += 1
        
        # Zusammenfassung ausgeben
        self.stdout.write("\nZusammenfassung:")
        self.stdout.write(self.style.SUCCESS(f"Erfolgreich aktualisiert: {updated_count} Zeitfenster"))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f"Übersprungene Lehrer: {skipped_count}"))
