from django.db import models

# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField(blank=True)
    ordering = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["ordering"]
        verbose_name = ("FAQ-Question")
        verbose_name_plural = ("FAQ-Questions")

    def __str__(self):
        return self.title