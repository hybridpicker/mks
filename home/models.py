from django.db import models
from ckeditor.fields import RichTextField

class IndexText(models.Model):
    lead_paragraph = models.TextField(blank=True)
    content = RichTextField(blank=True)

    def __str__(self):
        return 'IndexText'
