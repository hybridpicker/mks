from django.contrib import admin
from .models import Teacher, GroupPhoto
from .lesson_form import LessonForm
from .subject import Subject, SubjectCategory

# Register your models here.
admin.site.register(SubjectCategory)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(LessonForm)
admin.site.register(GroupPhoto)
