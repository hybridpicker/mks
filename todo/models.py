from django.db import models
from django.utils import timezone
from users.models import CustomUser
from .priority import PriorityChoicesField
from django.utils.translation import gettext as _
from django.core.exceptions import MultipleObjectsReturned

class Category(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = ("Todo Category")
        verbose_name_plural = ("Todo Categories")
        ordering = ["name",]
    def __str__(self):
        return self.name

class TodoList(models.Model):
    title = models.CharField(max_length=250)
    priority = PriorityChoicesField(_("Priority"),
                                    null=True, blank=True)
    content = models.TextField(blank=True)
    created = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)

    class Meta:
        ordering = ["priority", "due_date", "created"]
        verbose_name = ("Todo List Item")
        verbose_name_plural = ("Todo List Items")

    def __str__(self):
        return self.title

'''
Class for saving finished Tasks
'''
class FinishedItems(models.Model):
    done_date = models.DateField(null=True, blank=True)
    done_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    created_by_id = models.IntegerField(blank=True, null=True)
    priority = PriorityChoicesField(_("Priority"),
                                    null=True, blank=True)

    def save(self, *args, **kwargs):
        finished_content = self.content
        finished_due = self.due_date
        priority = self.priority
        try:
            todo = TodoList.objects.get(content=finished_content,
                                        due_date=finished_due,
                                        priority=priority,
                                        )
            todo.delete()
        except TodoList.DoesNotExist:
            pass
        except TodoList.MultipleObjectsReturned:
            pass
        super(FinishedItems, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        verbose_name = ("Finished Task Item")
        verbose_name_plural = ("Finished Task Items")

    def __str__(self):
        return self.title
