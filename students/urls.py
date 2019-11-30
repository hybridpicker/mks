from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signInView, name='students_signin'),
    path('signin/success/', views.successView, name='student_successfully_saved'),
]
