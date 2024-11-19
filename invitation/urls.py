from django.urls import path
from . import views

app_name = 'invitation'

urlpatterns = [
    path('', views.invitation_view, name='invitation_form'),
    path('danke/', views.thank_you_view, name='thank_you'),
    path('anmeldungen/', views.invitation_list_view, name='invitation_list'),
]
