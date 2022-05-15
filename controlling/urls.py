from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from .views import get_all_students, get_student

urlpatterns = [
    path('students', views.get_all_students, name='get_controlling_student'),
    path('coordinator/students', views.get_all_students_coordinator, name='get_controlling_students_coordinator'),
    path('single_student', views.get_student, name='get_controlling_single_student'),
    path('index_text', views.get_index_text, name='get_index_text')
]
