# Generated by Django 2.2.8 on 2019-12-16 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20191214_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(blank=True, max_length=120, null=True),
        ),
    ]