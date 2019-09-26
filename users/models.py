from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(_(u'First Name'), max_length=30)
    last_name = models.CharField(_(u'Last Name'), max_length=30)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'
