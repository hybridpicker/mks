# Generated by Django 4.0.4 on 2022-05-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0014_teacher_subject_coordinator'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='coordinator',
            field=models.ManyToManyField(blank=True, to='teaching.subjectcategory'),
        ),
    ]