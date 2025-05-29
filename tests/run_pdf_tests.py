#!/usr/bin/env python
"""
Test runner script for student PDF generator tests
Usage: python run_pdf_tests.py
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

if __name__ == "__main__":
    from django.test.runner import DiscoverRunner
    
    test_runner = DiscoverRunner(verbosity=2, interactive=True)
    
    # Run specific test module
    failures = test_runner.run_tests(['tests.test_student_pdf_generator'])
    
    if failures:
        sys.exit(1)
    else:
        print("\n✅ All PDF generator tests passed!")
