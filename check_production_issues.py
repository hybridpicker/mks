#!/usr/bin/env python
"""
Skript zur Überprüfung potentieller Production-Probleme
"""
import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

print("=== PRODUCTION ISSUE CHECKER ===\n")

# 1. Check imports
print("1. Checking critical imports...")
try:
    import xhtml2pdf
    print(f"✓ xhtml2pdf version: {xhtml2pdf.__version__}")
except ImportError as e:
    print(f"✗ xhtml2pdf import error: {e}")

try:
    import reportlab
    print(f"✓ reportlab version: {reportlab.Version}")
except ImportError as e:
    print(f"✗ reportlab import error: {e}")

try:
    from xhtml2pdf import pisa
    print("✓ pisa import successful")
except ImportError as e:
    print(f"✗ pisa import error: {e}")

# 2. Check PDF-specific imports
print("\n2. Checking PDF template dependencies...")
try:
    from django.template.loader import get_template
    template = get_template('controlling/single_student_pdf.html')
    print("✓ PDF template found and loaded")
except Exception as e:
    print(f"✗ PDF template error: {e}")

# 3. Check static files
print("\n3. Checking static files configuration...")
from django.conf import settings
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")

# 4. Check memory-intensive operations
print("\n4. Checking for memory issues...")
try:
    # Test PDF generation with minimal content
    from django.http import HttpResponse
    from xhtml2pdf import pisa
    
    html = "<html><body><h1>Test</h1></body></html>"
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        print(f"✗ PDF generation error: {pisa_status.err}")
    else:
        print("✓ PDF generation test successful")
except Exception as e:
    print(f"✗ PDF generation exception: {e}")

# 5. Check circular imports
print("\n5. Checking for circular imports...")
try:
    from controlling import views
    print("✓ controlling.views import successful")
except ImportError as e:
    print(f"✗ controlling.views import error: {e}")

# 6. Check middleware issues
print("\n6. Checking middleware configuration...")
for middleware in settings.MIDDLEWARE:
    try:
        module_path, class_name = middleware.rsplit('.', 1)
        __import__(module_path)
        print(f"✓ {middleware}")
    except Exception as e:
        print(f"✗ {middleware}: {e}")

# 7. Check database connection
print("\n7. Checking database connection...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database error: {e}")

# 8. Check for version conflicts
print("\n8. Checking version compatibility...")
import django
print(f"Django version: {django.VERSION}")
print(f"Python version: {sys.version}")

# 9. Check specific view function
print("\n9. Testing PDF view function...")
try:
    from controlling.views import generate_student_pdf
    print("✓ generate_student_pdf function imported successfully")
    
    # Check if function has proper attributes
    if hasattr(generate_student_pdf, '__wrapped__'):
        print("✓ Function has decorators applied")
except Exception as e:
    print(f"✗ PDF view function error: {e}")

print("\n=== CHECK COMPLETE ===")
