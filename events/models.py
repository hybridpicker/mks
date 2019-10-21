import datetime
from django.db import models
from django.utils.translation import gettext as _
from location.models import Country
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

# Create your models here.

class Event(models.Model):
    '''
    Model holding events data
    '''
    name = models.CharField(_(u'Name of Event'), max_length=50)
    image = models.ImageField(
        upload_to='events/images/',
        default='event_default.jpg', blank=True)
    venue = models.CharField(_(u'Venue'), max_length=50, blank=True)
    date = models.DateField(
        _("date for event"),
        default=datetime.date.today, blank=True)
    time = models.TimeField(_("Event Time "), db_index=True,
                            null=True, blank=True)
    link = models.URLField(
        _("Link"),
        max_length=128,
        db_index=True,
        unique=True,
        blank=True
    )
    def __str__(self):
        return '%s: %s' % (self.name, self.date)

    def get_date_presentation(self):
        tp = self.date
        day = tp.strftime('%d')
        month = tp.strftime('%m')
        return str(day + '|' + month)

    def get_time_presentation(self):
        tp = self.time
        hour = tp.strftime('%H')
        minutes = tp.strftime('%M')
        return str(hour + ':' + minutes + ' Uhr')

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Student
        '''
        ordering = ('date',)
        verbose_name = u'Event'
        verbose_name_plural = u'Events'
