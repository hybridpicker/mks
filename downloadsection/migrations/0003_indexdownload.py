# Generated by Django 3.0.3 on 2020-05-10 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloadsection', '0002_auto_20191207_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='material name')),
                ('thumbnail', models.ImageField(blank=True, default='downloadsection_imageDefault', upload_to='downloadsection/images/')),
                ('file', models.FileField(blank=True, upload_to='downloadsection/files')),
                ('ordering', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Index-Download',
                'verbose_name_plural': 'Index-Downloads',
                'ordering': ['ordering', 'name'],
            },
        ),
    ]