from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from .views import get_all_students, get_student

urlpatterns = [
    path('students', views.get_all_students, name='get_controlling_student'),
    path('single_student', views.get_student, name='get_controlling_single_student'),
]
