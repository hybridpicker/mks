"""
Central URL configuration for navbar links
Provides a clean way to manage all navigation URLs in one place
"""

from django.urls import reverse
from django.utils.safestring import mark_safe

class NavbarUrls:
    """Central URL resolver for navbar links"""
    
    @staticmethod
    def get_urls():
        """Return a dictionary of all navbar URLs"""
        try:
            return {
                # Main navigation
                'home': reverse('home_view'),
                'musikschule': reverse('teaching:teaching_music'),
                'kunstschule': reverse('teaching:teaching_art'),
                'galerie': reverse('gallery_view'),
                'ueber_uns': reverse('teaching:all_teachers'),
                'kontakt': reverse('contact_email'),
                
                # Musikschule subpages
                'blasinstrumente': reverse('teaching:teaching_brass'),
                'eme': reverse('teaching:teaching_eme'),
                'musikkunde': reverse('teaching:teaching_theory'),
                'schlaginstrumente': reverse('teaching:teaching_drums'),
                'stimmbildung': reverse('teaching:teaching_vocal'),
                'streichinstrumente': reverse('teaching:teaching_strings'),
                'tanz_bewegung': reverse('dance:schedule'),
                'tasteninstrumente': reverse('teaching:teaching_keys'),
                'zupfinstrumente': reverse('teaching:teaching_picked'),
                
                # Special offers
                'orgelunterricht': reverse('orgelunterricht'),
                'midi_band': reverse('midi_band'),
                'preise': reverse('teaching:teaching_prices'),
                
                # About us subpages
                'team': reverse('teaching:all_teachers'),
                'geschichte': reverse('history'),
                'blog': reverse('blog_summary'),
            }
        except Exception:
            # Fallback URLs if reverse fails
            return {
                'home': '/',
                'orgelunterricht': '/orgelunterricht/',
                'midi_band': '/midi-band/',
            }
