# Generated by Django 2.2.5 on 2019-12-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Slug'),
        ),
    ]