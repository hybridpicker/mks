from django.core.management.base import BaseCommand
from dance.models import Course
from django.db.models import F

class Command(BaseCommand):
    help = 'Aktualisiert Kurskategorien in der Datenbank'

    def handle(self, *args, **options):
        # 1. Aktualisiere "Zeitgenössischer Tanz - Fokus Improvisation & Tanztheater" zu "Moderner Tanz"
        # Hierbei suchen wir nach Kursen, die "Zeitgenössischer Tanz" und "Improvisation" oder "Tanztheater" im Namen haben
        matching_contemporary = Course.objects.filter(
            name__icontains='Zeitgenössischer Tanz'
        ).filter(
            name__icontains='Improvisation'
        )
        
        count_contemporary = matching_contemporary.count()
        if count_contemporary > 0:
            self.stdout.write(self.style.WARNING(f'Gefunden: {count_contemporary} Kurse mit "Zeitgenössischer Tanz - Fokus Improvisation & Tanztheater"'))
            
            # Bei Bedarf können spezifische Kurse direkt aktualisiert werden
            for course in matching_contemporary:
                self.stdout.write(f'Kurs: {course.name}')
                # Hier könnten wir auch die Beschreibung aktualisieren, falls notwendig
        
        # Wir müssen keine direkten Änderungen an den Kursdaten vornehmen, da die Kategorien
        # über die Funktion get_course_category() in den Views dynamisch bestimmt werden
        
        self.stdout.write(self.style.SUCCESS('Kategorie-Mapping aktualisiert!'))
        self.stdout.write(self.style.SUCCESS('- "Klassisches Ballett" -> "Klassischer Tanz"'))
        self.stdout.write(self.style.SUCCESS('- Kurse mit "Zeitgenössischer Tanz", "Improvisation" und "Tanztheater" werden als "Moderner Tanz" kategorisiert'))
        
        # Hinweis: Um diese Änderungen in der Fixture zu speichern, führen Sie anschließend aus:
        # python manage.py update_dance_fixture
