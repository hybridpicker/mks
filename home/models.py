from django.db import models
from ckeditor.fields import RichTextField

class IndexText(models.Model):
    lead_paragraph = models.TextField(blank=True)
    content = RichTextField(blank=True)

    def __str__(self):
        return 'IndexText'

class Alert(models.Model):
    title = models.CharField(max_length=255, default="Untitled")  # Titel für den Alert
    message = models.TextField()  # Längeres Textfeld für den Inhalt des Alerts
    is_active = models.BooleanField(default=False)  # Flag, um zu entscheiden, ob der Alert aktiv ist
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # Anzeige des Titels im Admin-Bereich
