from django.db import migrations
import os
from django.conf import settings
from django.core.management import call_command

def reload_fixture(apps, schema_editor):
    """Lädt das Fixture neu, um die vordefinierten Altersgruppen zu unterstützen."""
    # Hole alle Model-Klassen
    Teacher = apps.get_model('dance', 'Teacher')
    Course = apps.get_model('dance', 'Course')
    TimeSlot = apps.get_model('dance', 'TimeSlot')
    
    # Lösche alle vorhandenen Daten, um Duplikate zu vermeiden
    TimeSlot.objects.all().delete()
    Course.objects.all().delete()
    Teacher.objects.all().delete()
    
    # Lade die aktualisierten Daten
    fixture_name = 'dance_data.json'
    fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', fixture_name)
    
    if os.path.exists(fixture_path):
        call_command('loaddata', fixture_name, app_label='dance')

class Migration(migrations.Migration):
    """
    Leere Migration, die das Fixture neu lädt, um die neuen vordefinierten Altersgruppen zu unterstützen.
    Diese Migration wird ausgeführt, wenn ein git pull durchgeführt wird.
    """
    dependencies = [
        ('dance', '0002_timeslot_location'),
    ]

    operations = [
        migrations.RunPython(reload_fixture),
    ]
