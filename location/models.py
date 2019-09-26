'''
Models for Location
'''
from django.db import models
# Create your models here.

class Country(models.Model):
    '''
    Model holding countries
    '''
    country_name = models.CharField(max_length=30)
    def __str__(self):
        return str(self.country_name)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Country
        '''
        verbose_name = u'Country'
        verbose_name_plural = u'Countries'

class Location(models.Model):
    '''
    Model holding locations
    '''
    location_name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.location_name)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Location
        '''
        verbose_name = u'Location'
        verbose_name_plural = u'Locations'
