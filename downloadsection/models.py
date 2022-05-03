from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Forms(models.Model):
    name = models.CharField(_(u'material name'), max_length=50)
    thumbnail = models.ImageField(
        upload_to='downloadsection/images/',
        default='downloadsection_imageDefault', blank=True)
    file = models.FileField(upload_to='downloadsection/files', blank=True,)
    description = models.TextField(null=True, blank=True)
    ordering = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        '''
        Meta class for Forms
        '''
        ordering = ['ordering', 'name']
        verbose_name = u'Form'
        verbose_name_plural = u'Forms'

class IndexDownload(models.Model):
    name = models.CharField(_(u'material name'), max_length=50)
    thumbnail = models.ImageField(
        upload_to='downloadsection/images/',
        default='downloadsection_imageDefault', blank=True)
    file = models.FileField(upload_to='downloadsection/files', blank=True,)
    ordering = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        '''
        Meta class for Forms
        '''
        ordering = ['ordering', 'name']
        verbose_name = u'Index-Download'
        verbose_name_plural = u'Index-Downloads'
