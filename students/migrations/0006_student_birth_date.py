# Generated by Django 3.0.3 on 2020-04-21 16:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20191201_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='birth_date',
            field=models.DateField(blank=True, default=datetime.date.today, verbose_name='birth_date'),
        ),
    ]