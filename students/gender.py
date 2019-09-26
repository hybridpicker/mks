from django.utils.translation import gettext as _
from django.db import models

class Gender(models.Model):
    gender = models.CharField(_(u'gender'),max_length=6,)
    def __str__(self):
        return "%s" % (self.gender)
