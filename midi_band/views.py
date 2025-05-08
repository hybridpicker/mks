from django.shortcuts import render

def midi_band(request):
    """
    View function for midi-band page of site.
    
    This view displays information about the Midiband St.Pölten, 
    a youth orchestra for young musicians.
    """
    context = {
        'title': 'MIDI Band St.Pölten',
        'vimeo_id': '1082196370',  # Vimeo video ID
    }
    return render(request, 'midi_band/midi_band.html', context)
