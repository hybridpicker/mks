from django.urls import path
from django.shortcuts import render

app_name = 'maintenance'

def maintenance_view(request):
    """View für direkte Anzeige der Maintenance Page"""
    from .models import MaintenanceMode
    maintenance = MaintenanceMode.load()
    context = {
        'maintenance': maintenance,
        'hide_navbar': True,
        'hide_footer': True,
    }
    return render(request, 'maintenance/under_construction.html', context)

urlpatterns = [
    path('maintenance/', maintenance_view, name='maintenance_page'),
]