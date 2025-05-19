from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = HTMLField(blank=True)  # TinyMCE field like in Blog
    ordering = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["ordering"]
        verbose_name = ("FAQ-Question")
        verbose_name_plural = ("FAQ-Questions")

    def __str__(self):
        return self.question