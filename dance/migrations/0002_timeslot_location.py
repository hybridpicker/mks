from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='location',
            field=models.CharField(blank=True, help_text='Optional, z.B. Campus oder Kulturheim Spratzern', max_length=100, null=True, verbose_name='Standort'),
        ),
    ]
