#!/usr/bin/env python
"""
Django Test Command für Lazy Loading
Verwendung: python manage.py test gallery.tests -v 2
"""

# Erstelle eine Management Command für einfache Tests
import os
from django.core.management.base import BaseCommand
from django.test import Client
from gallery.models import Photo, PhotoCategory
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'Testet die Lazy Loading Implementation'

    def handle(self, *args, **options):
        self.stdout.write("\n🚀 Teste Lazy Loading Implementation...\n")
        
        client = Client()
        
        # Test 1: Gallery View
        response = client.get('/gallery/')
        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS('✅ Gallery View funktioniert'))
            
            # Test 2: Lazy Loading Integration
            content = response.content.decode('utf-8')
            
            if 'lazy-loading.js' in content:
                self.stdout.write(self.style.SUCCESS('✅ Lazy Loading JS gefunden'))
            else:
                self.stdout.write(self.style.ERROR('❌ Lazy Loading JS fehlt'))
                
            if 'data-src' in content:
                self.stdout.write(self.style.SUCCESS('✅ Data-src Attribute vorhanden'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  Data-src Attribute fehlen (keine Bilder?)'))
                
        else:
            self.stdout.write(self.style.ERROR(f'❌ Gallery View Fehler: {response.status_code}'))
        
        self.stdout.write(self.style.SUCCESS('\n✨ Test abgeschlossen!'))
