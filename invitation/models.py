# models.py

from django.db import models
from events.models import Event

class Invitation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Event-Beziehung - neue Implementierung
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    
    # Alte Felder für Rückwärtskompatibilität (deprecated)
    event_name = models.CharField(max_length=255, default="", blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    location = models.TextField(default="", null=True, blank=True)

    # Begleitpersonen
    number_of_guests = models.PositiveIntegerField(default=0, verbose_name="Anzahl der Begleitpersonen", null=True, blank=True)

    def __str__(self):
        if self.event:
            return f"{self.name} - {self.event.name}"
        return f"{self.name} - {self.email}"
    
    def get_event_name(self):
        """Gibt den Event-Namen zurück (bevorzugt aus Event-Objekt)"""
        if hasattr(self, 'event') and self.event:
            return self.event.name
        return self.event_name or "Unbekanntes Event"
    
    def get_event_date(self):
        """Gibt das Event-Datum zurück (bevorzugt aus Event-Objekt)"""
        if hasattr(self, 'event') and self.event:
            # Kombiniere Datum und Zeit zum DateTime-Objekt
            from datetime import datetime, time
            event_time = self.event.time if self.event.time else time(18, 0)  # Default 18:00
            return datetime.combine(self.event.date, event_time)
        return self.event_date
    
    def get_event_location(self):
        """Gibt den Event-Ort zurück (bevorzugt aus Event-Objekt)"""
        if hasattr(self, 'event') and self.event:
            return self.event.venue or "Ort noch nicht bekannt"
        return self.location or "Ort noch nicht bekannt"

