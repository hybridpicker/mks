# Generated by Django 3.0.3 on 2020-05-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indextext',
            name='lead_paragraph',
            field=models.TextField(blank=True),
        ),
    ]
