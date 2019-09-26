from django.db import models

class Subject(models.Model):
    subject = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.subject)
