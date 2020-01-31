from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import SmallIntegerField

CHOICES = {
    0 : _(u'Sehr Wichtig'),
    1 : _(u'Wichtig'),
    2 : _(u'Neutral'),
    3 : _(u'Nicht Wichtig'),
}

class PriorityChoicesField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(CHOICES.items()))
        super(PriorityChoicesField, self).__init__(*args, **kwargs)
