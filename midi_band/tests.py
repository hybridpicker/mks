from django.test import TestCase
from django.urls import reverse

class MidiBandViewTests(TestCase):
    def test_midi_band_view_exists(self):
        """
        Test that the midi_band view returns a 200 status code
        """
        response = self.client.get(reverse('midi_band'))
        self.assertEqual(response.status_code, 200)
        
    def test_midi_band_uses_correct_template(self):
        """
        Test that the midi_band view uses the correct template
        """
        response = self.client.get(reverse('midi_band'))
        self.assertTemplateUsed(response, 'midi_band/midi_band.html')
        
    def test_midi_band_content(self):
        """
        Test that the midi_band view contains the expected content
        """
        response = self.client.get(reverse('midi_band'))
        self.assertContains(response, 'Midiband St.Pölten')
        self.assertContains(response, 'NachwuchsmusikerInnen')
