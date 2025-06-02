#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('/Users/lukasschonsgibl/Coding/Django/mks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.urls import reverse, NoReverseMatch

def test_navbar_urls():
    urls_to_test = ['orgelunterricht', 'midi_band']
    results = []
    
    for url_name in urls_to_test:
        try:
            resolved_url = reverse(url_name)
            results.append(f"✅ {url_name} -> {resolved_url}")
        except NoReverseMatch as e:
            results.append(f"❌ {url_name} -> ERROR: {e}")
    
    return results

if __name__ == "__main__":
    print("Testing navbar URLs...")
    for result in test_navbar_urls():
        print(result)
