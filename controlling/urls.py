from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from . import views
from . import xlsviews
from .views import get_all_students, get_student

urlpatterns = [
    path('students', views.get_all_students, name='get_controlling_students'),
    path('coordinator/students', views.get_all_students_coordinator, name='get_controlling_students_coordinator'),
    path('single_student', views.get_student, name='get_controlling_single_student'),
    path('new_student', views.newStudentView, name='create_new_student'),
    path('parent', views.get_parent, name='get_controlling_parent'),
    path('coordinator/single_student', views.get_student_coordinator, name='get_controlling_single_student_coordinator'),
    path('index_text', views.get_index_text, name='get_index_text'),
    path('new_student/sucess', views.newStudentSuccessView, name='new_student_saved'),
    re_path(r'^export/xls/$', xlsviews.export_students_xls, name='export_students_xls'),
]
