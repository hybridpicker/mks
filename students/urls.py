from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('anmeldung/', views.signInView, name='students_signin'),
    path('anmeldung/erfolgreich/', views.successView, name='student_successfully_saved'),
]
