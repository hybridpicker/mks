# Generated by Django 3.1.13 on 2022-01-24 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0031_auto_20210921_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finisheditems',
            name='created',
            field=models.DateField(default='2022-01-24'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='done_date',
            field=models.DateField(default='2022-01-24'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='due_date',
            field=models.DateField(blank=True, default='2022-01-24', null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2022-01-24'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(blank=True, default='2022-01-24', null=True),
        ),
    ]
