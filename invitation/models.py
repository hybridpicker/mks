# models.py

from django.db import models

class Invitation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Neue Felder für die Veranstaltung
    event_name = models.CharField(max_length=255, default="Die Hexe Rabaukel bekommt Weihnachtspost")
    event_date = models.DateTimeField(null=True, blank=True)
    location = models.TextField(default="Grillparzercampus Orchestersaal, Grillparzerstraße 17, 3100 St. Pölten", null=True, blank=True)

    # Neues Feld für Begleitpersonen
    number_of_guests = models.PositiveIntegerField(default=0, verbose_name="Anzahl der Begleitpersonen", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
