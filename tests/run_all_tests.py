#!/usr/bin/env python
"""
Central test runner for MKS project tests.
Runs all tests in the organized test structure.
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import execute_from_command_line

def run_tests():
    """Run all tests in the tests package."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mks.settings")
    django.setup()
    
    # Test categories
    test_modules = [
        'tests.root_tests',
        'tests.app_tests',
        'tests.test_navbar_comprehensive',
        'tests.test_navbar_report', 
        'tests.test_pdf_template',
    ]
    
    print("Running MKS Project Tests...")
    print("=" * 50)
    
    # Run each test category
    for module in test_modules:
        print(f"\nRunning {module}...")
        execute_from_command_line(['manage.py', 'test', module])
    
    print("\n" + "=" * 50)
    print("All tests completed!")

if __name__ == '__main__':
    run_tests()
