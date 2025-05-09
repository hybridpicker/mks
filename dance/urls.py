from django.urls import path
from . import views

app_name = 'dance'

urlpatterns = [
    path('', views.dance_schedule_view, name='schedule'),
    path('wartung/', views.maintenance_view, name='maintenance'),
    path('lehrer-aktion/', views.teacher_action, name='teacher_action'),
    path('kurs-aktion/', views.course_action, name='course_action'),
    path('zeitfenster-aktion/', views.timeslot_action, name='timeslot_action'),
    path('loeschen/', views.delete_action, name='delete_action'),
    path('kurs/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Excel Import/Export
    path('excel-export/', views.export_excel, name='excel_export'),
    path('excel-import/', views.import_excel, name='excel_import'),
    
    # API-Endpunkte für die AJAX-Funktionalität
    path('api/lehrer/<int:teacher_id>/', views.teacher_detail_api, name='teacher_detail_api'),
    path('api/zeitfenster/<int:timeslot_id>/', views.timeslot_detail_api, name='timeslot_detail_api'),
]
