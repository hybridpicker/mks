# Generated by Django 3.0.3 on 2020-05-14 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0020_auto_20200511_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finisheditems',
            name='created',
            field=models.DateField(default='2020-05-14'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='done_date',
            field=models.DateField(default='2020-05-14'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='due_date',
            field=models.DateField(blank=True, default='2020-05-14', null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2020-05-14'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(blank=True, default='2020-05-14', null=True),
        ),
    ]