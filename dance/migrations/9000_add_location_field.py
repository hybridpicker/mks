from django.db import migrations, models, connection

# Diese Funktion führt sicheres SQL aus, das mit verschiedenen Datenbanken funktioniert
def safe_add_location_column(apps, schema_editor):
    cursor = connection.cursor()
    db_type = connection.vendor
    
    # Überprüfen, ob die Spalte existiert
    if db_type == 'mysql':
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = 'dance_timeslot' AND column_name = 'location' AND table_schema = DATABASE()"
        )
        column_exists = cursor.fetchone()[0] > 0
    elif db_type == 'postgresql':
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = 'dance_timeslot' AND column_name = 'location'"
        )
        column_exists = cursor.fetchone()[0] > 0
    elif db_type == 'sqlite':
        cursor.execute("PRAGMA table_info(dance_timeslot)")
        columns = cursor.fetchall()
        column_exists = any(column[1] == 'location' for column in columns)
    else:
        # Für andere Datenbanken verwenden wir den generischen Ansatz
        column_exists = False
    
    # Spalte hinzufügen, falls sie nicht existiert
    if not column_exists:
        if db_type == 'mysql':
            cursor.execute("ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100) NULL")
        elif db_type in ('postgresql', 'sqlite'):
            cursor.execute("ALTER TABLE dance_timeslot ADD COLUMN location VARCHAR(100)")

# Diese Funktion weist die Standorte basierend auf den Lehrern zu
def assign_locations(apps, schema_editor):
    TimeSlot = apps.get_model('dance', 'TimeSlot')
    Course = apps.get_model('dance', 'Course')
    Teacher = apps.get_model('dance', 'Teacher')
    
    # Zuweisungsregeln
    location_assignments = {}
    
    # Alle Lehrer durchgehen
    for teacher in Teacher.objects.all():
        location = 'Campus'  # Default-Standort
        
        # Spezifische Zuweisungen
        if 'Zeisel' in teacher.name or 'Bauer' in teacher.name:
            location = 'Campus'
        elif 'Usmanova' in teacher.name:
            location = 'Kulturhaus Wagram'
        elif 'Grüssinger' in teacher.name or 'Holzweber' in teacher.name:
            location = 'Kulturhaus Spratzern'
        
        location_assignments[teacher.id] = location
    
    # Zeitfenster aktualisieren
    for course in Course.objects.select_related('teacher').all():
        teacher_id = course.teacher_id
        location = location_assignments.get(teacher_id, 'Campus')
        
        TimeSlot.objects.filter(course=course).update(location=location)


class Migration(migrations.Migration):
    
    dependencies = [
        ('dance', '0001_initial'),
    ]
    
    operations = [
        # Spalte hinzufügen mit direktem SQL (sicher für alle Datenbanken)
        migrations.RunPython(safe_add_location_column),
        
        # Standorte zuweisen
        migrations.RunPython(assign_locations),
    ]
