from django.views.generic import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Instrument

# Create your views here.

def instruments_summary(request):
    all_blogs = Instrument.objects.all()
    context = {
        'all_instruments': all_instruments
        }
    return render(request, "instruments/summary.html", context)


class InstrumentView(View):
    def get(self, request, *args, **kwargs):
        instrument = get_object_or_404(Instrument, slug=kwargs['slug'])
        context = {'instrument': instrument}
        return render(request, 'instruments/instrument.html', context)
