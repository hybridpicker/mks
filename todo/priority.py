from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import SmallIntegerField

CHOICES = {
    0 : _(u'Sehr Hoch'),
    1 : _(u'Hoch'),
    2 : _(u'Mittel'),
    3 : _(u'Niedrig'),
}

class PriorityChoicesField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(CHOICES.items()))
        super(PriorityChoicesField, self).__init__(*args, **kwargs)
