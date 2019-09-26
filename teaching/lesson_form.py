from django.db import models
from django.utils.translation import gettext as _
from .subject import Subject

class LessonForm(models.Model):
    SINGLE = 'Einzelunterricht'
    GROUP = 'Gruppenunterricht'
    LESSON_CHOICES = (
        (SINGLE, 'Einzelunterricht'),
        (GROUP, 'Gruppenunterricht'),
    )
    lesson_form = models.CharField(_(u'Unterrichtsmodell'), max_length=20,
                                   choices=LESSON_CHOICES,)
    BLOCK_10 = '10'
    BLOCK_5 = '5'
    MONTHLY = 'Semestrierung'
    BILLING_CHOICES = (
        (BLOCK_10, '10er Block'),
        (BLOCK_5, '5er Block'),
        (MONTHLY, 'Monatlicher Betrag'),
    )
    billing_form = models.CharField(_(u'Verrechnungsmodel'), max_length=20,
                                    choices=BILLING_CHOICES,)
    MIN_25 = 25
    MIN_50 = 50
    UNITS_CHOICES = (
        (MIN_25, '25 Minuten'),
        (MIN_50, '50 Minuten'),
    )
    minutes = models.IntegerField(_(u'Minutenanzahl'),
                                  choices=UNITS_CHOICES,)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    price = models.DecimalField(_(u'Preis'), max_digits=5, decimal_places=2)

    def __str__(self):
        return "%s - %s - %s: %smin" % (self.lesson_form,
                                        self.subject,
                                        self.billing_form,
                                        self.minutes,)

    class Meta:
        ordering = ('subject',)
        verbose_name = u'Lessonform'
        verbose_name_plural = u'Lessonforms'
