# Generated by Django 2.2.5 on 2019-10-22 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='link',
            field=models.URLField(blank=True, db_index=True, max_length=128, verbose_name='Link'),
        ),
    ]
