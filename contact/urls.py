from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('kontakt/', views.emailView, name='contact_email'),
]

"""
    Url Needed for Google Captcha View
    path('contact/success/', views.successView, name='success_contact'),
"""
