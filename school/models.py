from django.db import models
from django.utils.translation import gettext as _
from location.models import Country

# Create your models here.

class MusicSchool(models.Model):
    '''
    Model holding music school data
    '''
    school_name = models.CharField(_(u'name of school'), max_length=50)
    school_logo = models.ImageField(
        upload_to='school/images/logo/',
        default='school_logo_imageDefault', blank=True)
    contact_email = models.EmailField(_(u'e-mail for contact'), max_length=70, blank=True)
    adress_line = models.CharField(_(u'street'), max_length=80, blank=True)
    house_number = models.CharField(_(u'house number'), max_length=80, blank=True)
    postal_code = models.CharField(_(u'postal code'), max_length=30, blank=True)
    city = models.CharField(_(u'city'), max_length=30, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s, %s' % (self.school_name, self.city)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Student
        '''
        ordering = ('school_name',)
        verbose_name = u'Music School'
        verbose_name_plural = u'Music Schools'
