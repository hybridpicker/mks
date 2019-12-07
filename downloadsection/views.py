from django.shortcuts import render
from .models import Forms

# Create your views here.
def pdf_forms_view(request):
    material_data = Forms.objects.all()
    context = {
        'material_data': material_data
    }
    return render(request, 'downloadsection/pdfs.html', context)
