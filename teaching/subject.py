from django.db import models

class SubjectCategory(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return "%s" % (self.name)

class Subject(models.Model):
    subject = models.CharField(max_length=80)
    category = models.ForeignKey(SubjectCategory, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.subject)
