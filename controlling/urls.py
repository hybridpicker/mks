from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from . import views
from . import xlsviews
from . import teacher_views
from .views import get_all_students, get_student

app_name = 'controlling'

urlpatterns = [
    # Student URLs
    path('students', views.get_all_students, name='get_controlling_students'),
    path('coordinator/students', views.get_all_students_coordinator, name='get_controlling_students_coordinator'),
    path('single_student', views.get_student, name='get_controlling_single_student'),
    path('new_student', views.newStudentView, name='create_new_student'),
    path('parent', views.get_parent, name='get_controlling_parent'),
    path('coordinator/single_student', views.get_student_coordinator, name='get_controlling_single_student_coordinator'),
    path('index_text', views.get_index_text, name='get_index_text'),
    path('new_student/sucess', views.newStudentSuccessView, name='new_student_saved'),
    re_path(r'^export/xls/$', xlsviews.export_students_xls, name='export_students_xls'),
    
    # Teacher Management URLs
    path('teachers', teacher_views.get_all_teachers, name='get_controlling_teachers'),
    path('teacher/<int:teacher_id>', teacher_views.get_teacher_detail, name='teacher_detail'),
    path('teacher/<int:teacher_id>/edit', teacher_views.teacher_quick_edit, name='teacher_quick_edit'),
    path('teacher/<int:teacher_id>/full-edit', teacher_views.teacher_full_edit, name='teacher_full_edit'),
    path('teacher/<int:teacher_id>/delete', teacher_views.teacher_delete, name='teacher_delete'),
    
    # Teacher API URLs
    path('api/teachers/search', teacher_views.teacher_api_search, name='teacher_api_search'),
    path('api/teachers/stats', teacher_views.teacher_stats_api, name='teacher_stats_api'),
]
