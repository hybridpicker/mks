import datetime
from django.db import models
from django.utils.translation import gettext as _
from location.models import Country
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

from projects.models import Project

# Create your models here.

class Event(models.Model):
    '''
    Model holding events data
    '''
    name = models.CharField(_(u'Name of Event'), max_length=100)
    image = models.ImageField(
        upload_to='events/images/',
        null=True,
        blank=True,
        help_text='Bild für die Veranstaltung. Optimal: 800x600px, max. 2MB.')
    venue = models.CharField(_(u'Venue'), max_length=80, blank=True)
    date = models.DateField(
        _("date for event"),
        default=datetime.date.today, blank=True)
    time = models.TimeField(_("Event Time "), db_index=True,
                            null=True, blank=True)
    link = models.URLField(
        _("Link"),
        max_length=128,
        db_index=True,
        blank=True
    )
    project = models.ForeignKey(
            'projects.Project',
            on_delete=models.CASCADE,
            blank=True, null=True)
    def __str__(self):
        return '%s: %s' % (self.name, self.date)
        
    def get_image_url(self):
        '''
        Returns the URL of the image if it exists and is not the default media image,
        otherwise returns the default static image URL.
        '''
        # Define the possible names for the default image in the media directory
        default_media_image_names = ['event_default.jpg', 'events/images/event_default.jpg']

        # Check if an image is uploaded AND its name is not one of the default media image names
        if self.image and hasattr(self.image, 'url') and self.image.name not in default_media_image_names:
            return self.image.url
        # Otherwise, return the static default image URL
        return '/static/events/event_default.jpg'

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
        Meta class for Event
        '''
        ordering = ('date',)
        verbose_name = u'Event'
        verbose_name_plural = u'Events'
