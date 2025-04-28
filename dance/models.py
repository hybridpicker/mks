from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Kontakt E-Mail"), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Lehrkraft")
        verbose_name_plural = _("Lehrkräfte")

class Course(models.Model):
    name = models.CharField(_("Kursname"), max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses', verbose_name=_("Lehrkraft"))
    age_group = models.CharField(_("Altersgruppe"), max_length=50)
    description = models.TextField(_("Beschreibung"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Kurs")
        verbose_name_plural = _("Kurse")

class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        ('Montag', _('Montag')),
        ('Dienstag', _('Dienstag')),
        ('Mittwoch', _('Mittwoch')),
        ('Donnerstag', _('Donnerstag')),
        ('Freitag', _('Freitag')),
        ('Samstag', _('Samstag')),
        ('Sonntag', _('Sonntag')),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timeslots', verbose_name=_("Kurs"))
    day = models.CharField(_("Tag"), max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(_("Startzeit"))
    end_time = models.TimeField(_("Endzeit"))
    studio = models.CharField(_("Studio"), max_length=50, blank=True, null=True, help_text=_("Optional, z.B. Studio 1")) # Optional studio field
    location = models.CharField(_("Standort"), max_length=100, blank=True, null=True, help_text=_("Optional, z.B. Campus oder Kulturheim Spratzern")) # Optional location field

    def __str__(self):
        return f"{self.course.name} - {self.get_day_display()} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"

    class Meta:
        verbose_name = _("Zeitfenster")
        verbose_name_plural = _("Zeitfenster")
        ordering = ['day', 'start_time'] # Default ordering
