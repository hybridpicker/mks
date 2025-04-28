from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dance', '0003_merge_0002_timeslot_location_update_fixture_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='location',
            field=models.CharField(blank=True, help_text='Optional, z.B. Campus oder Kulturheim Spratzern', max_length=100, null=True, verbose_name='Standort'),
        ),
    ]
