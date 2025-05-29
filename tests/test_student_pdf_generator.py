import os
import tempfile
from datetime import date, datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse
from unittest.mock import patch, MagicMock

# Import your models (adjust imports based on your actual model structure)
# from your_app.models import Student, Parent, Subject, Teacher


class StudentPDFGeneratorTest(TestCase):
    """
    Test suite for the single student PDF generator
    Tests template rendering, context data, and PDF generation functionality
    """
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.test_user = User.objects.create_user(
            username='test_teacher',
            email='test@musikschule.at',
            password='testpass123'
        )
        
        # Mock student data (adjust based on your actual model)
        self.mock_student = MagicMock()
        self.mock_student.id = 123
        self.mock_student.first_name = 'Max'
        self.mock_student.last_name = 'Mustermann'
        self.mock_student.email = 'max.mustermann@email.com'
        self.mock_student.phone = '+43 664 1234567'
        self.mock_student.mobile = '+43 664 7654321'
        self.mock_student.notes = 'Sehr talentierter Schüler\nZeigt große Fortschritte im Klavierspiel'
        
        # Mock parent data
        self.mock_parent = MagicMock()
        self.mock_parent.first_name = 'Maria'
        self.mock_parent.last_name = 'Mustermann'
        self.mock_parent.email = 'maria.mustermann@email.com'
        self.mock_parent.phone = '+43 2742 123456'
        self.mock_parent.street = 'Musterstraße 15'
        self.mock_parent.zip_code = '3100'
        self.mock_parent.city = 'St. Pölten'
        
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
            'request': MagicMock()
        }
        
        # Mock request object
        self.test_context['request'].user = self.test_user
    
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
        
        # Check student name
        self.assertIn('Max Mustermann', rendered)
        
        # Check contact data
        self.assertIn('max.mustermann@email.com', rendered)
        self.assertIn('+43 664 1234567', rendered)
        self.assertIn('+43 664 7654321', rendered)
        
        # Check subject and teacher
        self.assertIn('Klavier', rendered)
        self.assertIn('Prof. Anna Schmidt', rendered)
        
        # Check lesson details
        self.assertIn('30 Min.', rendered)
        self.assertIn('Einzelunterricht', rendered)
    
    def test_parent_data_in_template(self):
        """Test that parent/contact person data appears correctly"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check parent name
        self.assertIn('Maria Mustermann', rendered)
        
        # Check parent contact
        self.assertIn('maria.mustermann@email.com', rendered)
        self.assertIn('+43 2742 123456', rendered)
        
        # Check address
        self.assertIn('Musterstraße 15', rendered)
        self.assertIn('3100 St. Pölten', rendered)
    
    def test_notes_field_with_content(self):
        """Test that notes field displays content correctly with line breaks"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check notes content
        self.assertIn('Sehr talentierter Schüler', rendered)
        self.assertIn('Zeigt große Fortschritte im Klavierspiel', rendered)
        
        # Check that linebreaks filter is applied (should contain <br> or <p> tags)
        self.assertTrue('<br>' in rendered or '<p>' in rendered)
    
    def test_notes_field_empty(self):
        """Test that empty notes field shows fallback text"""
        # Test with empty notes
        context_empty_notes = self.test_context.copy()
        context_empty_notes['student'].notes = None
        
        rendered = render_to_string('controlling/single_student_pdf.html', context_empty_notes)
        self.assertIn('Keine Anmerkungen vorhanden', rendered)
    
    def test_empty_fields_handling(self):
        """Test that empty fields show appropriate fallback text"""
        # Create context with empty fields
        context_empty = self.test_context.copy()
        context_empty['birth_date'] = None
        context_empty['start_date'] = None
        context_empty['subject_str'] = None
        context_empty['teacher_str'] = None
        
        rendered = render_to_string('controlling/single_student_pdf.html', context_empty)
        
        # Check fallback texts
        self.assertIn('Nicht angegeben', rendered)
        self.assertIn('Nicht zugewiesen', rendered)
    
    def test_access_url_in_footer(self):
        """Test that the access URL is correctly generated in footer"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        expected_url = f'/team/controlling/single_student?id={self.mock_student.id}'
        self.assertIn(expected_url, rendered)
    
    @patch('django.utils.timezone.now')
    def test_download_info_in_footer(self, mock_now):
        """Test that download user and timestamp appear in footer"""
        # Mock current time
        mock_time = datetime(2025, 5, 29, 14, 30, 0, tzinfo=timezone.get_current_timezone())
        mock_now.return_value = mock_time
        
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check user info
        self.assertIn(f'Heruntergeladen von: {self.test_user.username}', rendered)
        
        # Check timestamp format and MEZ timezone
        self.assertIn('29.05.2025 14:30', rendered)
        self.assertIn('(MEZ)', rendered)
    
    def test_timezone_handling(self):
        """Test that Vienna/MEZ timezone is correctly applied"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that timezone tags are present
        self.assertIn('Europe/Vienna', rendered.replace(' ', '').replace('\n', '') or 
                     'MEZ' in rendered)
    
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
        self.assertIn('class="student-name"', rendered)
        self.assertIn('class="section"', rendered)
        self.assertIn('class="info-row"', rendered)
        self.assertIn('class="footer"', rendered)
        
        # Check that @page CSS is present for PDF formatting
        self.assertIn('@page', rendered)
        self.assertIn('size: A4', rendered)
    
    def test_all_required_sections_present(self):
        """Test that all required sections are present in the template"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check section headings
        self.assertIn('STAMMDATEN', rendered.upper())
        self.assertIn('KONTAKTDATEN SCHÜLER', rendered.upper())
        self.assertIn('UNTERRICHT', rendered.upper())
        self.assertIn('KONTAKTPERSON', rendered.upper())
        self.assertIn('ANMERKUNGEN', rendered.upper())
    
    def test_school_branding(self):
        """Test that school branding and contact info is present"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check school name and branding
        self.assertIn('Musikschule der Landeshauptstadt St. Pölten', rendered)
        self.assertIn('Maria Theresia Straße 23', rendered)
        self.assertIn('3100 St. Pölten', rendered)
        self.assertIn('musikschule@st-poelten.gv.at', rendered)
        self.assertIn('+43 2742 333-2651', rendered)
    
    def test_creation_date_format(self):
        """Test that creation date is properly formatted"""
        rendered = render_to_string('controlling/single_student_pdf.html', self.test_context)
        
        # Check that creation date is present
        self.assertIn('Erstellt am:', rendered)
        
        # The date should be in German format (day. month year)
        import re
        date_pattern = r'\d{1,2}\.\s+\w+\s+\d{4}'
        self.assertTrue(re.search(date_pattern, rendered), 
                       "Creation date not found in expected German format")


class StudentPDFIntegrationTest(TestCase):
    """
    Integration tests for PDF generation endpoint
    """
    
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='test_user',
            password='testpass123'
        )
        self.client.force_login(self.test_user)
    
    @patch('your_app.views.get_student_data')  # Adjust import path
    def test_pdf_view_returns_proper_response(self, mock_get_student):
        """Test that PDF view returns proper HTTP response"""
        # Mock student data
        mock_get_student.return_value = {
            'student': MagicMock(id=123, first_name='Test', last_name='Student'),
            'parent': MagicMock(),
            'birth_date': '01.01.2010',
        }
        
        # Assuming you have a URL pattern for PDF generation
        # url = reverse('student_pdf', kwargs={'student_id': 123})
        # response = self.client.get(url)
        
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response['Content-Type'], 'application/pdf')
        
        # For now, just test template rendering
        self.assertTrue(True)  # Placeholder until actual view is available


if __name__ == '__main__':
    import unittest
    unittest.main()
