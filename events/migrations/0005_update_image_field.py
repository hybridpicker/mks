# Generated manually

from django.db import migrations, models

class Migration(migrations.Migration):
    """
    This migration updates the Event model to handle missing images gracefully
    """

    dependencies = [
        ('events', '0004_event_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                help_text='Bild für die Veranstaltung. Optimal: 800x600px, max. 2MB.',
                upload_to='events/images/'
            ),
        ),
    ]
