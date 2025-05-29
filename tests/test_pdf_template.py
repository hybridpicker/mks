import os
from django.test import TestCase
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


class MockStudent:
    """Simple mock object for student data"""
    def __init__(self):
        self.id = 123
        self.first_name = 'Max'
        self.last_name = 'Mustermann'
        self.email = 'max.mustermann@email.com'
        self.phone = '+43 664 1234567'
        self.mobile = '+43 664 7654321'
        self.notes = 'Sehr talentierter Schüler\nZeigt große Fortschritte im Klavierspiel'


class MockParent:
    """Simple mock object for parent data"""
    def __init__(self):
        self.first_name = 'Maria'
        self.last_name = 'Mustermann'
        self.email = 'maria.mustermann@email.com'
        self.phone = '+43 2742 123456'
        self.street = 'Musterstraße 15'
        self.zip_code = '3100'
        self.city = 'St. Pölten'


class MockRequest:
    """Simple mock object for request"""
    def __init__(self, user):
        self.user = user


class StudentPDFTemplateTest(TestCase):
    """
    Simplified test suite for the single student PDF template
    Tests only template rendering without PDF generation dependencies
    """
    
    def setUp(self):
        """Set up test data"""
        
        # Create test user
        self.test_user = User.objects.create_user(
            username='test_teacher',
            email='test@musikschule.at',
            password='testpass123'
        )
        
        # Create mock objects
        self.mock_student = MockStudent()
        self.mock_parent = MockParent()
        self.mock_request = MockRequest(self.test_user)
        
        # Mock context data
        self.test_context = {
            'student': self.mock_student,
            'parent': self.mock_parent,
            'birth_date': '15.03.2010',
            'start_date': '01.09.2020',
            'subject_str': 'Klavier',
            'teacher_str': 'Prof. Anna Schmidt',
            'lesson_duration': 30,
            'lesson_type': 'Einzelunterricht',
            'request': self.mock_request
        }
    
    def test_template_exists(self):
        """Test that the PDF template file exists"""
        template_path = '/Users/lukasschonsgibl/Coding/Django/mks/templates/controlling/single_student_pdf.html'
        self.assertTrue(os.path.exists(template_path), 
                       f"Template file does not exist: {template_path}")
    
    def test_template_renders_without_errors(self):
        """Test that template renders without syntax errors"""
        try:
            rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
            self.assertIsInstance(rendered, str)
            self.assertGreater(len(rendered), 0)
        except Exception as e:
            self.fail(f"Template failed to render: {str(e)}")
    
    def test_student_data_in_template(self):
        """Test that student data appears correctly in rendered template"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that the template renders and contains expected data
        self.assertIn('Max', rendered)  # Student first name
        self.assertIn('Mustermann', rendered)  # Student last name
        self.assertIn('Klavier', rendered)  # Subject
        self.assertIn('Prof. Anna Schmidt', rendered)  # Teacher
        self.assertIn('30 Min.', rendered)  # Lesson duration
        self.assertIn('Einzelunterricht', rendered)  # Lesson type
    
    def test_parent_data_in_template(self):
        """Test that parent/contact person data appears correctly"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that parent section exists and contains data
        self.assertIn('Kontaktperson', rendered)
        self.assertIn('Maria', rendered)  # Parent first name
        self.assertIn('Mustermann', rendered)  # Parent last name
        self.assertIn('maria.mustermann@email.com', rendered)  # Parent email
        self.assertIn('+43 2742 123456', rendered)  # Parent phone
        self.assertIn('Musterstraße 15', rendered)  # Parent street
        self.assertIn('3100', rendered)  # Parent zip code
        self.assertIn('St. Pölten', rendered)  # Parent city
    
    def test_notes_field_with_content(self):
        """Test that notes field displays content correctly"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that notes section exists and contains notes
        self.assertIn('Anmerkungen', rendered)
        self.assertIn('Sehr talentierter Schüler', rendered)  # Part of notes content
        self.assertIn('Zeigt große Fortschritte im Klavierspiel', rendered)  # Part of notes content
        self.assertIn('min-height: 80px', rendered)  # Check styling is applied
        self.assertIn('background-color: #f8f9fa', rendered)  # Check background styling
    
    def test_notes_field_empty(self):
        """Test that empty notes field shows fallback text"""
        # Create a student with empty notes
        self.mock_student.notes = None
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that fallback text appears
        self.assertIn('Keine Anmerkungen vorhanden', rendered)
    
    def test_access_url_in_footer(self):
        """Test that the access URL is correctly generated in footer"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that the URL structure is present with the student ID
        self.assertIn('Zugriff via: /team/controlling/single_student?id=123', rendered)
    
    def test_download_info_in_footer(self):
        """Test that download user info appears in footer"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that download structure is present with username
        self.assertIn('Heruntergeladen von: test_teacher', rendered)
    
    def test_html_structure_and_styling(self):
        """Test that HTML structure and CSS classes are present"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check essential HTML structure
        self.assertIn('<!DOCTYPE html>', rendered)
        self.assertIn('<html>', rendered)
        self.assertIn('<head>', rendered)
        self.assertIn('<body>', rendered)
        
        # Check CSS classes
        self.assertIn('class="header"', rendered)
        self.assertIn('class="section"', rendered)
        self.assertIn('class="info-row"', rendered)
        self.assertIn('class="footer"', rendered)
        
        # Check that @page CSS is present for PDF formatting
        self.assertIn('@page', rendered)
        self.assertIn('size: A4', rendered)
    
    def test_all_required_sections_present(self):
        """Test that all required sections are present in the template"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check section headings (case insensitive)
        rendered_upper = rendered.upper()
        self.assertIn('STAMMDATEN', rendered_upper)
        self.assertIn('KONTAKTDATEN', rendered_upper)
        self.assertIn('UNTERRICHT', rendered_upper)
        self.assertIn('KONTAKTPERSON', rendered_upper)
        self.assertIn('ANMERKUNGEN', rendered_upper)
    
    def test_school_branding(self):
        """Test that school branding and contact info is present"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check school name and branding
        self.assertIn('Musikschule der Landeshauptstadt St. Pölten', rendered)
        self.assertIn('Maria Theresia Straße 23', rendered)
        self.assertIn('3100 St. Pölten', rendered)
        self.assertIn('musikschule@st-poelten.gv.at', rendered)
        self.assertIn('+43 2742 333-2651', rendered)
    
    def test_creation_date_present(self):
        """Test that creation date is present"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that creation date is present
        self.assertIn('Erstellt am:', rendered)


if __name__ == '__main__':
    import unittest
    unittest.main()
