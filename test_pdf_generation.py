#!/usr/bin/env python
"""
Test PDF generation locally
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mks.settings')
django.setup()

from students.models import Student
from django.test import RequestFactory
from controlling.views import generate_student_pdf
from django.contrib.auth import get_user_model

User = get_user_model()

def test_pdf_generation():
    """Test PDF generation with a sample student"""
    try:
        # Create a fake request
        factory = RequestFactory()
        request = factory.get('/test-pdf/')
        
        # Add a user to the request (required for login_required decorator)
        user = User.objects.filter(is_staff=True).first()
        if not user:
            print("No staff user found. Please create one first.")
            return
        
        request.user = user
        
        # Get first student
        student = Student.objects.first()
        if not student:
            print("No student found in database.")
            return
        
        print(f"Testing PDF generation for student: {student.first_name} {student.last_name}")
        
        # Generate PDF
        response = generate_student_pdf(request, student.id)
        
        if response.status_code == 200:
            print("✓ PDF generated successfully!")
            print(f"  Content-Type: {response['Content-Type']}")
            print(f"  Content-Disposition: {response['Content-Disposition']}")
            print(f"  PDF size: {len(response.content)} bytes")
            
            # Save PDF locally for inspection
            filename = f"test_student_{student.id}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  PDF saved as: {filename}")
        else:
            print(f"✗ PDF generation failed with status code: {response.status_code}")
            print(f"  Response: {response.content.decode('utf-8')}")
            
    except Exception as e:
        print(f"✗ Error during PDF generation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()
