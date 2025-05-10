# Generated manually

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alert'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('content', models.TextField(max_length=250, verbose_name='Content')),
                ('icon', models.CharField(choices=[('music', 'Musik'), ('award', 'Auszeichnung'), ('calendar-alt', 'Kalender'), ('graduation-cap', 'Bildung'), ('users', 'Gruppe'), ('bullhorn', 'Ankündigung'), ('star', 'Wichtig'), ('info-circle', 'Information')], default='info-circle', max_length=20, verbose_name='Icon')),
                ('date_added', models.DateField(default=django.utils.timezone.now, verbose_name='Date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Display Order')),
            ],
            options={
                'verbose_name': 'News Item',
                'verbose_name_plural': 'News Items',
                'ordering': ['-date_added', 'order'],
            },
        ),
        migrations.AlterModelOptions(
            name='alert',
            options={'verbose_name': 'Alert', 'verbose_name_plural': 'Alerts'},
        ),
        migrations.AlterModelOptions(
            name='indextext',
            options={'verbose_name': 'Index Text', 'verbose_name_plural': 'Index Texts'},
        ),
        migrations.AlterField(
            model_name='alert',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.TextField(verbose_name='Alert Message'),
        ),
        migrations.AlterField(
            model_name='alert',
            name='title',
            field=models.CharField(default='Untitled', max_length=255, verbose_name='Alert Title'),
        ),
        migrations.AlterField(
            model_name='indextext',
            name='content',
            field=models.TextField(verbose_name='Content of Index page'),
        ),
        migrations.AlterField(
            model_name='indextext',
            name='lead_paragraph',
            field=models.TextField(blank=True, verbose_name='Lead paragraph'),
        ),
    ]