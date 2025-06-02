#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('/Users/lukasschonsgibl/Coding/Django/mks')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from django.urls import reverse
from django.urls import NoReverseMatch

def test_unified_navbar_urls():
    """Test all URLs used in the unified navbar"""
    
    urls_to_test = [
        # Public URLs
        'home_view',
        'teaching:teaching_music',
        'teaching:teaching_brass',
        'teaching:teaching_eme', 
        'teaching:teaching_theory',
        'teaching:teaching_drums',
        'teaching:teaching_vocal',
        'teaching:teaching_strings',
        'dance:schedule',
        'teaching:teaching_keys',
        'teaching:teaching_picked',
        'orgelunterricht',  # This was the main problem!
        'midi_band',       # This was also fixed!
        'teaching:teaching_prices',
        'teaching:teaching_art',
        'gallery_view',
        'teaching:all_teachers',
        'history',
        'blog_summary',
        'contact_email',
        
        # Admin URLs
        'users:team',
        'show_blogs_editing',
        'get_all_faqs',
        'controlling:get_index_text',
        'controlling:get_controlling_students',
        'invitation:invitation_list',
        'users:event_managing_view',
        'gallery_admin',
        'users:logout',
    ]
    
    results = []
    failed_urls = []
    
    for url_name in urls_to_test:
        try:
            resolved_url = reverse(url_name)
            results.append(f"✅ {url_name:<35} -> {resolved_url}")
        except NoReverseMatch as e:
            results.append(f"❌ {url_name:<35} -> ERROR: {e}")
            failed_urls.append(url_name)
    
    return results, failed_urls

if __name__ == "__main__":
    print("Testing Unified Navbar URLs...")
    print("=" * 80)
    
    results, failed_urls = test_unified_navbar_urls()
    
    for result in results:
        print(result)
    
    print("=" * 80)
    print(f"Test completed! {len(failed_urls)} failed URLs")
    
    if failed_urls:
        print("\nFailed URLs:")
        for url in failed_urls:
            print(f"  - {url}")
