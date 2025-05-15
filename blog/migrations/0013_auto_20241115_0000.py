# Generated manually
from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_blogpost_number_of_posts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image_alt_text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='meta_description',
            field=models.TextField(max_length=160),
        ),
    ]