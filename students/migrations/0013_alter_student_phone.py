# Generated by Django 4.0.4 on 2022-05-29 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_alter_student_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=70, verbose_name='telephone_number'),
        ),
    ]