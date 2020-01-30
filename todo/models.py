from django.db import models
from django.utils import timezone
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()

    class Meta:
        verbose_name = ("Todo Category")
        verbose_name_plural = ("Todo Categories")
    def __str__(self):
        return self.name

class TodoList(models.Model):
    title = models.CharField(max_length=250)
    priority = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"), null=True, blank=True)
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
        ordering = ["-priority", "due_date","created"]
        verbose_name = ("Todo List Item")
        verbose_name_plural = ("Todo List Items")

    def __str__(self):
        return self.title

'''
Class for saving finished Tasks
'''
class FinishedItems(models.Model):
    done_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    done_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"), null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    created_by_id = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        finished_content = self.content
        finished_due = self.due_date
        try:
            todo = TodoList.objects.get(content=finished_content, due_date=finished_due)
            print(todo)
            todo.delete()
        except TodoList.DoesNotExist:
            pass
        super(FinishedItems, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        verbose_name = ("Finished Task Item")
        verbose_name_plural = ("Finished Task Items")

    def __str__(self):
        return self.title
