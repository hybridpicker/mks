# Generated by Django 3.0.2 on 2020-02-01 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20200131_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['priority', 'due_date', 'created'], 'verbose_name': 'Todo List Item', 'verbose_name_plural': 'Todo List Items'},
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='created',
            field=models.DateField(default='2020-02-01'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='done_date',
            field=models.DateField(default='2020-02-01'),
        ),
        migrations.AlterField(
            model_name='finisheditems',
            name='due_date',
            field=models.DateField(blank=True, default='2020-02-01', null=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateField(default='2020-02-01'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(blank=True, default='2020-02-01', null=True),
        ),
    ]