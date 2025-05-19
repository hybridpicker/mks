from django.urls import path
from . import views, admin_views

app_name = 'invitation'

urlpatterns = [
    path('', views.invitation_view, name='invitation_form'),
    path('danke/', views.thank_you_view, name='thank_you'),
    path('anmeldungen/', views.invitation_list_view, name='invitation_list'),
    
    # Admin-URLs
    path('admin/', admin_views.invitation_admin_dashboard, name='admin_dashboard'),
    path('admin/edit/', admin_views.invitation_event_edit, name='admin_edit_all'),
    path('admin/invitation/<int:invitation_id>/', admin_views.invitation_detail_edit, name='admin_edit_invitation'),
    path('admin/create/', admin_views.invitation_create, name='admin_create'),
]
