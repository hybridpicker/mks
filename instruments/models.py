from django.db import models
from tinymce.models import HTMLField
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

class Instrument(models.Model):
    instrument_name = models.CharField(max_length=60)
    image = models.ImageField(
        upload_to='instruments/images',
        default='instruments_imageDefault', blank=True,)
    content = HTMLField()
    meta_title = models.CharField(max_length=60)
    meta_description = models.TextField()
    slug = models.SlugField(_("slug"), max_length=200, unique=True)

    def __str__(self):
        return '%s' % (self.instrument_name)

    class Meta:
        '''
        Meta class for Author
        '''
        ordering = ('instrument_name',)
        verbose_name = u'Instrument'
        verbose_name_plural = u'Instruments'
