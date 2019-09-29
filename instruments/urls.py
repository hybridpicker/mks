from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('all_instruments', views.instruments_summary, name='instruments_summary'),
    path('<slug>/', views.InstrumentView.as_view(), name='instrument_description'),
]
