# Generated manually for adding Event relationship to Invitation

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),  # Assumes events app has initial migration
        ('invitation', '0003_invitation_number_of_guests_and_more'),  # Last invitation migration
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='event_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='location',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
