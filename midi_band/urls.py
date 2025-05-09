from django.urls import path
from . import views

urlpatterns = [
    path('', views.midi_band, name='midi_band'),
]
