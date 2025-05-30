from django.db import models
from django.core.cache import cache

class MaintenanceMode(models.Model):
    """Singleton Model für Maintenance Mode Einstellungen"""
    is_active = models.BooleanField(
        default=False,
        help_text="Aktiviert den Wartungsmodus für normale Benutzer"
    )
    title = models.CharField(
        max_length=200,
        default="Wartungsarbeiten",
        help_text="Titel der Wartungsseite"
    )
    message = models.TextField(
        default="Wir führen gerade ein Update durch und sind bald wieder für Sie da!",
        help_text="Nachricht die auf der Wartungsseite angezeigt wird"
    )
    expected_downtime = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Erwartete Dauer der Wartung (z.B. '2 Stunden')"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wartungsmodus"
        verbose_name_plural = "Wartungsmodus"

    def save(self, *args, **kwargs):
        # Singleton Pattern - nur eine Instanz erlaubt
        self.pk = 1
        super().save(*args, **kwargs)
        # Cache invalidieren wenn Status geändert wird
        cache.delete('maintenance_mode_status')

    def delete(self, *args, **kwargs):
        # Verhindere das Löschen
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Wartungsmodus: {'Aktiv' if self.is_active else 'Inaktiv'}"