#!/usr/bin/env python
"""
Test Runner für Lazy Loading Implementation
Führt alle wichtigen Tests aus
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mks.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Führe spezifische Gallery Tests aus
    failures = test_runner.run_tests([
        "gallery.tests.test_lazy_loading",
        "gallery.tests.test_frontend",
    ])
    
    if failures:
        sys.exit(1)
    else:
        print("\n✅ Alle Lazy Loading Tests erfolgreich!")