# Generated by Django 3.2.12 on 2022-02-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0009_auto_20200705_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(blank=True, default='gallery_imageDefault.jpg', upload_to='gallery/images/'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image_lazy',
            field=models.ImageField(blank=True, default='gallery_lazy_imageDefault.jpg', upload_to='gallery/images/lazy/'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image_thumbnail',
            field=models.ImageField(blank=True, default='gallery_thumbnail_imageDefault.jpg', upload_to='gallery/images/thumbnail'),
        ),
    ]
