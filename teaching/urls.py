from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from . import views
import teaching.get_students
from teaching.get_students import get_all_students, get_student
from teaching.show_teacher_view import show_teacher_view

urlpatterns = [
    path('allstudents', teaching.get_students.get_all_students, name='get_all_students'),
    path('singlestudent', teaching.get_students.get_student, name='get_student'),
    path('all_teachers', teaching.show_teacher_view.show_teacher_view, name="all_teachers")
]
