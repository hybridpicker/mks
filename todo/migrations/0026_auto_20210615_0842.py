# Generated by Django 3.0.7 on 2021-06-15 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0025_auto_20210531_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finisheditems',
            name='created',
            field=models.DateField(default='2021-06-15'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='done_date',
            field=models.DateField(default='2021-06-15'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='due_date',
            field=models.DateField(blank=True, default='2021-06-15', null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2021-06-15'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(blank=True, default='2021-06-15', null=True),
        ),
    ]
