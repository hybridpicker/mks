from django.db import models

class SubjectCategory(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return "%s" % (self.name)

    class Meta: # pylint: disable=too-few-public-methods
        '''
        Meta class for Subject Category
        '''
        ordering = ('name',)

class Subject(models.Model):
    subject = models.CharField(max_length=80)
    category = models.ForeignKey(SubjectCategory, on_delete=models.CASCADE)
    ordering = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.subject)

    class Meta: # pylint: disable=too-few-public-methods
        '''
        Meta class for Subject
        '''
        ordering = ('ordering',)
        verbose_name = u'Subject'
        verbose_name_plural = u'Subjects'
