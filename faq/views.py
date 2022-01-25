from django.shortcuts import render
from faq.models import FAQ

# Create your views here.
def faq_view (request):
    faq = FAQ.objects.all()
    context = {
        'faq': faq,
    }
    return render (request, 'faq/faq.html', context)