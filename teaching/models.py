'''
Class holding teacher data
'''
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from phone_field import PhoneField
from location.models import Location, Country
from users.models import CustomUser
from teaching.subject import Subject, SubjectCategory


class GroupPhoto(models.Model):
    image = models.ImageField(
        upload_to='teachers/images/', blank=True,)
    mobile_image = models.ImageField(
        upload_to='teachers/images/mobile/', blank=True,)
        
    class Meta: # pylint: disable=too-few-public-methods
        '''
        Meta class for GroupPhoto
        '''
        ordering = ('image',)
        verbose_name = u'Group Photo'
        verbose_name_plural = u'Group Photos'


class Teacher(models.Model):
    '''
    Model holding teacher data
    '''
    gender = models.ForeignKey('students.Gender', on_delete=models.CASCADE)
    academic_title = models.ForeignKey(
        'students.AcademicTitle',
        on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(_(u'Vorname'), max_length=30)
    last_name = models.CharField(_(u'Nachname'), max_length=30)
    subject = models.ManyToManyField(
              Subject,
              blank=True)
    subject_coordinator = models.ManyToManyField(
              SubjectCategory,
              blank=True)
    subject_coordinator_active = models.BooleanField(
              default=True, 
              verbose_name=_('Fachgruppenleitung aktiv'),
              help_text=_('Bestimmt ob die Fachgruppenleitung aktiv ist'))
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    image = models.ImageField(
        upload_to='teachers/images/',
        default='teachers/teacher_image_default.svg', blank=True,)
    lazy_image = models.ImageField(
        upload_to='teachers/images/lazy/',
        default='teachers/teacher_image_default.svg', blank=True,)
    email = models.EmailField(blank=True)
    homepage = models.URLField(_(u'Deine Website'), blank=True, max_length=80)
    phone = PhoneField(_(u'Telefonnummer'), blank=True, default='+43 ', help_text='Telefonnummer')
    adress_line = models.CharField(_(u'Straße'), max_length=80, blank=True)
    house_number = models.CharField(_(u'Hausnummer'), max_length=80, blank=True)
    postal_code = models.CharField(_(u'Postleitzahl'), max_length=4, blank=True)
    city = models.CharField(_(u'Wohnort'), max_length=30, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True,)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True,blank=True,)
    bio = models.TextField(null=True, blank=True)
    youtube_id_one = models.CharField(_(u'Youtube Video ID 1'), max_length=24, blank=True)
    youtube_id_two = models.CharField(_(u'Youtube Video ID 2'), max_length=24, blank=True)

    def homepage_adress(self):
        hp = self.homepage.replace('https://', '').replace('http://', '').replace('/', '')
        return hp

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta: # pylint: disable=too-few-public-methods
        '''
        Meta class for Teacher
        '''
        ordering = ('last_name',)
        verbose_name = u'Teacher'
        verbose_name_plural = u'Teacher'
