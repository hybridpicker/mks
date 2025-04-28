from django.db import migrations, models

def check_and_add_location_column(apps, schema_editor):
    """Überprüft, ob die location-Spalte existiert und fügt sie hinzu, falls nicht."""
    # Verbindung zur Datenbank
    connection = schema_editor.connection
    cursor = connection.cursor()
    
    # Überprüfen, ob die Spalte existiert
    table_name = 'dance_timeslot'
    column_name = 'location'
    column_exists = False
    
    # Abfrage je nach Datenbanktyp
    if connection.vendor == 'mysql':
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = %s AND column_name = %s AND table_schema = DATABASE()",
            [table_name, column_name]
        )
        column_exists = cursor.fetchone()[0] > 0
    elif connection.vendor == 'postgresql':
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.columns "
            "WHERE table_name = %s AND column_name = %s",
            [table_name, column_name]
        )
        column_exists = cursor.fetchone()[0] > 0
    elif connection.vendor == 'sqlite':
        cursor.execute(f"PRAGMA table_info({table_name})")
        column_exists = any(col[1] == column_name for col in cursor.fetchall())
    
    # Spalte hinzufügen, falls sie nicht existiert
    if not column_exists:
        if connection.vendor == 'mysql':
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(100) NULL"
            )
        elif connection.vendor == 'postgresql':
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(100) NULL"
            )
        elif connection.vendor == 'sqlite':
            cursor.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(100)"
            )

def assign_locations(apps, schema_editor):
    """Weist Standorte zu den Zeitfenstern basierend auf den Lehrern zu."""
    # Modelle laden
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

class Migration(migrations.Migration):
    """
    Diese Migration stellt sicher, dass die location-Spalte in der Tabelle dance_timeslot existiert
    und die Standorte korrekt zugewiesen sind.
    
    Sie hat keine spezifischen Abhängigkeiten und sollte in jedem Zustand funktionieren.
    """
    dependencies = [
        # Abhängigkeit zu einer grundlegenden Migration, die garantiert existiert
        ('dance', '0001_initial'),
    ]

    operations = [
        # Führt die SQL-Operation aus, um die Spalte hinzuzufügen, falls sie nicht existiert
        migrations.RunPython(check_and_add_location_column),
        
        # Weist Standorte den Lehrern zu
        migrations.RunPython(assign_locations),
        
        # Wir verwenden SeparateDatabaseAndState, um das Modell zu aktualisieren, 
        # ohne die Datenbank zu verändern (die Spalte wurde bereits hinzugefügt)
        migrations.SeparateDatabaseAndState(
            # Keine Datenbankänderung
            database_operations=[],
            
            # Nur Änderung am Modellstatus
            state_operations=[
                migrations.AddField(
                    model_name='timeslot',
                    name='location',
                    field=models.CharField(blank=True, help_text='Optional, z.B. Campus oder Kulturheim Spratzern', max_length=100, null=True, verbose_name='Standort'),
                ),
            ],
        ),
    ]
