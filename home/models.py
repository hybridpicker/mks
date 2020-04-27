from django.db import models
from ckeditor.fields import RichTextField

class IndexText(models.Model):
    content = RichTextField(blank=True)

    def __str__(self):
        return 'IndexText'
