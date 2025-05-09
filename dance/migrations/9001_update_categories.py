from django.db import migrations
from django.db.models import F, Q

def update_categories(apps, schema_editor):
    """Update course categories in the database."""
    Course = apps.get_model('dance', 'Course')
    
    # 1. Find courses with 'Klassisches Ballett' in description and update them
    for course in Course.objects.filter(description__icontains='Klassisches Ballett'):
        course.description = course.description.replace('Klassisches Ballett', 'Klassischer Tanz')
        course.save()
    
    # 2. Find courses with 'Klassisches Ballett' in name and update them
    for course in Course.objects.filter(name__icontains='Klassisches Ballett'):
        course.name = course.name.replace('Klassisches Ballett', 'Klassischer Tanz')
        course.save()
    
    # The "Zeitgenössischer Tanz - Fokus Improvisation & Tanztheater" categorization
    # is handled by the get_course_category function in views.py, and doesn't need
    # a database update since the category is computed dynamically.

class Migration(migrations.Migration):
    dependencies = [
        ('dance', '0002_timeslot_location'),
    ]

    operations = [
        migrations.RunPython(update_categories),
    ]
