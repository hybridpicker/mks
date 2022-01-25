from django.shortcuts import render
from faq.models import FAQ

# Create your views here.
def faq_view (request):
    faqs = FAQ.objects.all()
    context = {
        'faqs': faqs,
    }
    return render (request, 'faq/faq.html', context)