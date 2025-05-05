from django.db import migrations
import json
import os
from django.conf import settings
from django.core.management import call_command

def update_fixture(apps, schema_editor):
    """Update the dance_data.json file with the current database state."""
    # Path to the fixture file
    fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', 'dance_data.json')
    
    if os.path.exists(fixture_path):
        try:
            # Export current data to the fixture file
            # This ensures the fixture reflects the database changes from previous migrations
            with open(fixture_path, 'w', encoding='utf-8') as f:
                call_command('dumpdata', 'dance.Teacher', 'dance.Course', 'dance.TimeSlot',
                            indent=4, stdout=f)
            
            # Verify fixture data by loading it
            with open(fixture_path, 'r', encoding='utf-8') as f:
                fixture_data = json.load(f)
                
            # Confirm data was written correctly
            course_count = sum(1 for item in fixture_data if item.get('model') == 'dance.course')
            teacher_count = sum(1 for item in fixture_data if item.get('model') == 'dance.teacher')
            timeslot_count = sum(1 for item in fixture_data if item.get('model') == 'dance.timeslot')
            
            print(f"Updated fixture file with: {teacher_count} teachers, {course_count} courses, {timeslot_count} timeslots")
            
        except Exception as e:
            print(f"Error updating fixture file: {str(e)}")
    else:
        print(f"Fixture file not found: {fixture_path}")

class Migration(migrations.Migration):
    dependencies = [
        ('dance', '9001_update_categories'),
    ]

    operations = [
        migrations.RunPython(update_fixture),
    ]
