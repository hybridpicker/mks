#!/usr/bin/env python
"""
Debug script to identify potential causes for "Incomplete response received from application" error
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

def check_pdf_dependencies():
    """Check if PDF generation dependencies are properly installed"""
    print("=== PDF Dependencies Check ===")
    try:
        import xhtml2pdf
        print(f"✓ xhtml2pdf version: {xhtml2pdf.__version__}")
    except ImportError as e:
        print(f"✗ xhtml2pdf import failed: {e}")
    
    try:
        import reportlab
        print(f"✓ reportlab version: {reportlab.Version}")
    except ImportError as e:
        print(f"✗ reportlab import failed: {e}")
    
    try:
        import html5lib
        print(f"✓ html5lib imported successfully")
    except ImportError as e:
        print(f"✗ html5lib import failed: {e}")
    
    try:
        import PyPDF2
        print(f"✓ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"✗ PyPDF2 import failed: {e}")

def check_settings():
    """Check Django settings that might cause timeout issues"""
    print("\n=== Django Settings Check ===")
    from django.conf import settings
    
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"FILE_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 'Not set')}")
    print(f"DATA_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 'Not set')}")
    print(f"DATA_UPLOAD_MAX_NUMBER_FIELDS: {getattr(settings, 'DATA_UPLOAD_MAX_NUMBER_FIELDS', 'Not set')}")
    
    # Check for common timeout-related settings
    print(f"CONN_MAX_AGE: {settings.DATABASES['default'].get('CONN_MAX_AGE', 'Not set')}")

def check_middleware():
    """Check for problematic middleware"""
    print("\n=== Middleware Check ===")
    from django.conf import settings
    
    for middleware in settings.MIDDLEWARE:
        print(f"- {middleware}")
        if 'TwoFactor' in middleware and '#' not in middleware:
            print("  ⚠️  Two-factor middleware is active - might cause redirects")

def check_urls():
    """Check for URL configuration issues"""
    print("\n=== URL Configuration Check ===")
    try:
        from django.urls import reverse
        # Try to reverse the PDF generation URL
        try:
            url = reverse('controlling:generate_student_pdf', args=[1])
            print(f"✓ PDF URL resolves: {url}")
        except Exception as e:
            print(f"✗ PDF URL error: {e}")
    except Exception as e:
        print(f"✗ URL check failed: {e}")

def check_static_files():
    """Check static files configuration"""
    print("\n=== Static Files Check ===")
    from django.conf import settings
    
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    
    # Check if static directories exist
    for static_dir in settings.STATICFILES_DIRS:
        if os.path.exists(static_dir):
            print(f"✓ Static directory exists: {static_dir}")
        else:
            print(f"✗ Static directory missing: {static_dir}")

def check_logs():
    """Check recent errors in logs"""
    print("\n=== Recent Log Errors ===")
    log_file = os.path.join(os.path.dirname(__file__), 'logs', 'django.log')
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            error_lines = [line for line in lines[-100:] if 'ERROR' in line or 'TypeError' in line]
            if error_lines:
                print("Recent errors found:")
                for line in error_lines[-5:]:  # Show last 5 errors
                    print(f"  {line.strip()}")
            else:
                print("No recent errors in log file")
    else:
        print("Log file not found")

if __name__ == "__main__":
    print("Django MKS - Debugging 'Incomplete response' error\n")
    
    check_pdf_dependencies()
    check_settings()
    check_middleware()
    check_urls()
    check_static_files()
    check_logs()
    
    print("\n=== Recommendations ===")
    print("1. Ensure all PDF dependencies are installed: pip install -r requirements.txt")
    print("2. Check server logs for timeout errors")
    print("3. Verify WSGI/Gunicorn timeout settings on the server")
    print("4. Monitor memory usage during PDF generation")
    print("5. Consider simplifying the PDF template CSS")
