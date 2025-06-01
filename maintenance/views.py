from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json
from .models import MaintenanceMode

@require_POST
@user_passes_test(lambda u: u.is_superuser)
def toggle_maintenance(request):
    """Toggle Maintenance Mode via AJAX"""
    try:
        data = json.loads(request.body)
        is_active = data.get('is_active', False)
        
        maintenance = MaintenanceMode.load()
        maintenance.is_active = is_active
        maintenance.save()
        
        return JsonResponse({
            'success': True,
            'is_active': maintenance.is_active,
            'message': f'Wartungsmodus {"aktiviert" if is_active else "deaktiviert"}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
