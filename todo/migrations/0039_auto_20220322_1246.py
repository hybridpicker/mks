# Generated by Django 3.2.12 on 2022-03-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0038_auto_20220221_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finisheditems',
            name='created',
            field=models.DateField(default='2022-03-22'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='done_date',
            field=models.DateField(default='2022-03-22'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='due_date',
            field=models.DateField(blank=True, default='2022-03-22', null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2022-03-22'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(blank=True, default='2022-03-22', null=True),
        ),
    ]
