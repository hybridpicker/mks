# Generated by Django 4.0.4 on 2022-05-16 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_alter_parent_first_name_alter_parent_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='trial_lesson',
            field=models.BooleanField(default=False),
        ),
    ]
