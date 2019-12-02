from django.contrib import admin

# Register your models here.
from .models import Student, Parent
from .academic_title import AcademicTitle
from .gender import Gender

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(AcademicTitle)
admin.site.register(Gender)
