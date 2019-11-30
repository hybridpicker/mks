'''
Class for holding Student model
'''
import datetime
from django.utils.translation import gettext as _
from django.db import models
from phone_field import PhoneField
from location.models import Location, Country
from teaching.lesson_form import LessonForm
from teaching.subject import Subject
from .academic_title import AcademicTitle
from .gender import Gender
from .day_of_weeks import DayOfTheWeekField


class Student(models.Model):
    '''
    Model holding student data
    '''
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,
                               blank=True,
                               null=True)
    academic_title = models.ForeignKey(
        AcademicTitle,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    first_name = models.CharField(_(u'first name'), max_length=30)
    last_name = models.CharField(_(u'last name'), max_length=30)
    image = models.ImageField(
        upload_to='students/images/',
        default='student_imageDefault', blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(
        'teaching.Teacher',
        on_delete=models.CASCADE, blank=True, null=True)
    lesson_form = models.ForeignKey(
        LessonForm,
        on_delete=models.CASCADE, blank=True, null=True)
    regular_lesson_time = models.TimeField(_("regular lesson time "), db_index=True,
                                           help_text='if lessonform is monthly',
                                           null=True, blank=True)
    regular_lesson_day = DayOfTheWeekField(_("regular lesson day"),
                                           help_text='if lessonform is monthly',
                                           null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    lesson_count = models.IntegerField(_(u'lesson counter',), default=0)
    start_date = models.DateField(
        _("start date"),
        default=datetime.date.today, blank=True)
    phone = PhoneField(_(u'telephone number'),
                       blank=True, default='+43 ', help_text='Telefonnummer')
    email = models.EmailField(_(u'e-mail'), max_length=70, blank=True)
    iban = models.CharField(_(u'IBAN'), max_length=20, blank=True)
    bic = models.CharField(_(u'BIC'), max_length=20, blank=True)
    adress_line = models.CharField(_(u'street'), max_length=80, blank=True)
    house_number = models.CharField(_(u'house number'), max_length=80, blank=True)
    postal_code = models.CharField(_(u'postal code'), max_length=30, blank=True)
    city = models.CharField(_(u'city'), max_length=30, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:  # pylint: disable=too-few-public-methods
        '''
        Meta class for Student
        '''
        ordering = ('last_name',)
        verbose_name = u'Student'
        verbose_name_plural = u'Students'
