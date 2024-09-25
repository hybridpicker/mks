from django.urls import path
from . import views

app_name = 'invitation'

urlpatterns = [
    path('grillparzercampus/zusage/', views.invitation_view, name='invitation_form'),
    path('grillparzercampus/danke/', views.thank_you_view, name='thank_you'),
    path('grillparzercampus/anmeldungen/', views.invitation_list_view, name='invitation_list'),
]
