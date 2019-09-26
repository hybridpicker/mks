from django.utils.translation import gettext as _
from django.db import models

class AcademicTitle(models.Model):
    academic_title = models.CharField(_(u'Titel'),max_length=4,)
    def __str__(self):
        return "%s" % (self.academic_title)
    class Meta:
        verbose_name = u'academic title'
        verbose_name_plural = u'academic titles'
