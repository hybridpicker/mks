from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from . import views
import teaching.get_students
from teaching.get_students import get_all_students, get_student
from teaching.views import calendar_request

urlpatterns = [
    path('calendar', teaching.views.calendar_request, name='teaching_calendar'),
    path('allstudents', teaching.get_students.get_all_students, name='get_all_students'),
    path('singlestudent', teaching.get_students.get_student, name='get_student'),
]
