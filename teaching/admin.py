from django.contrib import admin
from .models import Teacher
from .lesson_form import LessonForm
from .subject import Subject

# Register your models here.
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(LessonForm)
