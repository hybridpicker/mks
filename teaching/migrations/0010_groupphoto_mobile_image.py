# Generated by Django 3.0.3 on 2020-05-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0009_groupphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupphoto',
            name='mobile_image',
            field=models.ImageField(blank=True, upload_to='teachers/images/mobile/'),
        ),
    ]
