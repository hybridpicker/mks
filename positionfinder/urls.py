from django.urls import path
import positionfinder.views_scale
import positionfinder.views_arpeggio
import positionfinder.views_chords

urlpatterns = [
    path('', positionfinder.views_scale.fretboard_scale_view, name='show_scale_fretboard'),
    path('arpeggios', positionfinder.views_arpeggio.fretboard_arpeggio_view,
         name='show_arpeggio_fretboard'),
    path('chords', positionfinder.views_chords.fretboard_chords_view,
         name='show_chords_fretboard'),
]
