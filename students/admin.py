from django.contrib import admin

# Register your models here.
from .models import Student
from .academic_title import AcademicTitle
from .gender import Gender

admin.site.register(Student)
admin.site.register(AcademicTitle)
admin.site.register(Gender)
