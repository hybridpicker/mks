# Generated by Django 3.2.12 on 2022-04-10 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teaching', '0012_subject_hidden_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ('ordering', '-complementary_subject', 'subject'), 'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
    ]
