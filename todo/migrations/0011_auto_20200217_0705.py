# Generated by Django 3.0.3 on 2020-02-17 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_auto_20200206_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finisheditems',
            name='created',
            field=models.DateField(default='2020-02-17'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='done_date',
            field=models.DateField(default='2020-02-17'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='due_date',
            field=models.DateField(blank=True, default='2020-02-17', null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2020-02-17'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(blank=True, default='2020-02-17', null=True),
        ),
    ]
