from django.db import migrations

def assign_locations(apps, schema_editor):
    """Weist Standorte zu den Zeitfenstern basierend auf den Lehrern zu."""
    # Modell laden
    TimeSlot = apps.get_model('dance', 'TimeSlot')
    Course = apps.get_model('dance', 'Course')
    Teacher = apps.get_model('dance', 'Teacher')
    
    # Zuweisungsregeln
    teacher_location_map = {
        'Zeisel': 'Campus',
        'Bauer': 'Campus',
        'Usmanova': 'Kulturhaus Wagram',
        'Grüssinger': 'Kulturhaus Spratzern',
        'Holzweber': 'Kulturhaus Spratzern',
    }
    
    # Alle Lehrer durchgehen
    for teacher in Teacher.objects.all():
        # Standort für diesen Lehrer finden
        location = None
        for teacher_name, loc in teacher_location_map.items():
            if teacher_name.lower() in teacher.name.lower():
                location = loc
                break
        
        # Wenn kein expliziter Match gefunden wurde, versuchen wir einen intelligenten Default
        if location is None:
            # Default-Standort "Campus" für nicht explizit zugewiesene Lehrer
            location = 'Campus'
        
        # Alle Kurse des Lehrers finden
        for course in Course.objects.filter(teacher=teacher):
            # Alle Zeitfenster für diesen Kurs aktualisieren
            TimeSlot.objects.filter(course=course).update(location=location)

def reverse_assign_locations(apps, schema_editor):
    """Entfernt alle zugewiesenen Standorte."""
    TimeSlot = apps.get_model('dance', 'TimeSlot')
    TimeSlot.objects.all().update(location=None)

class Migration(migrations.Migration):
    dependencies = [
        ('dance', '0004_timeslot_location_for_production'),
    ]

    operations = [
        migrations.RunPython(assign_locations, reverse_assign_locations),
    ]
