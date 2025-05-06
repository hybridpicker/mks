import os
import tempfile
import json
from datetime import time
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd
from .models import Teacher, Course, TimeSlot
from .excel_utils import export_to_excel, parse_excel_file, generate_fixture_from_excel_data, update_database_from_fixture


class ExcelUtilsTestCase(TestCase):
    """Test cases for Excel import/export functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create test teachers
        self.teacher1 = Teacher.objects.create(
            name="Test Teacher 1",
            email="teacher1@test.com"
        )
        self.teacher2 = Teacher.objects.create(
            name="Test Teacher 2",
            email="teacher2@test.com"
        )
        
        # Create test courses
        self.course1 = Course.objects.create(
            name="Test Course 1",
            teacher=self.teacher1,
            age_group="6-8 Jahre",
            description="Test course description 1"
        )
        self.course2 = Course.objects.create(
            name="Test Course 2",
            teacher=self.teacher2,
            age_group="10-12 Jahre",
            description="Test course description 2"
        )
        
        # Create test timeslots
        self.timeslot1 = TimeSlot.objects.create(
            course=self.course1,
            day="Montag",
            start_time=time(14, 0),
            end_time=time(15, 30),
            studio="Studio 1",
            location="Campus"
        )
        self.timeslot2 = TimeSlot.objects.create(
            course=self.course2,
            day="Dienstag",
            start_time=time(16, 0),
            end_time=time(17, 30),
            studio=None,
            location="Kulturhaus Spratzern"
        )
        
        # Create directory for excel exports if it doesn't exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'excel_exports'), exist_ok=True)
    
    def test_export_to_excel(self):
        """Test exporting data to Excel"""
        # Export data to Excel
        excel_path = export_to_excel()
        
        # Check if file exists
        full_path = os.path.join(settings.BASE_DIR, excel_path)
        self.assertTrue(os.path.exists(full_path))
        
        # Read the Excel file to check its contents
        xl = pd.ExcelFile(full_path)
        
        # Check if all sheets exist
        self.assertIn('Teachers', xl.sheet_names)
        self.assertIn('Courses', xl.sheet_names)
        self.assertIn('TimeSlots', xl.sheet_names)
        
        # Read the sheets
        df_teachers = pd.read_excel(xl, sheet_name='Teachers')
        df_courses = pd.read_excel(xl, sheet_name='Courses')
        df_timeslots = pd.read_excel(xl, sheet_name='TimeSlots')
        
        # Check teachers data
        self.assertEqual(len(df_teachers), 2)
        self.assertIn('id', df_teachers.columns)
        self.assertIn('name', df_teachers.columns)
        self.assertIn('email', df_teachers.columns)
        
        # Check courses data
        self.assertEqual(len(df_courses), 2)
        self.assertIn('id', df_courses.columns)
        self.assertIn('name', df_courses.columns)
        self.assertIn('teacher_id', df_courses.columns)
        self.assertIn('teacher_name', df_courses.columns)
        self.assertIn('age_group', df_courses.columns)
        self.assertIn('description', df_courses.columns)
        
        # Check timeslots data
        self.assertEqual(len(df_timeslots), 2)
        self.assertIn('id', df_timeslots.columns)
        self.assertIn('course_id', df_timeslots.columns)
        self.assertIn('course_name', df_timeslots.columns)
        self.assertIn('day', df_timeslots.columns)
        self.assertIn('start_time', df_timeslots.columns)
        self.assertIn('end_time', df_timeslots.columns)
        self.assertIn('studio', df_timeslots.columns)
        self.assertIn('location', df_timeslots.columns)
        
        # Clean up the file
        os.remove(full_path)
    
    def test_parse_excel_file(self):
        """Test parsing Excel file"""
        # First export data to create a valid Excel file
        excel_path = export_to_excel()
        full_path = os.path.join(settings.BASE_DIR, excel_path)
        
        # Parse the Excel file
        excel_data = parse_excel_file(full_path)
        
        # Check if data was parsed correctly
        self.assertIn('teachers', excel_data)
        self.assertIn('courses', excel_data)
        self.assertIn('timeslots', excel_data)
        
        self.assertEqual(len(excel_data['teachers']), 2)
        self.assertEqual(len(excel_data['courses']), 2)
        self.assertEqual(len(excel_data['timeslots']), 2)
        
        # Clean up the file
        os.remove(full_path)
    
    def test_generate_fixture_from_excel_data(self):
        """Test generating fixture from Excel data"""
        # First export data to create a valid Excel file
        excel_path = export_to_excel()
        full_path = os.path.join(settings.BASE_DIR, excel_path)
        
        # Parse the Excel file
        excel_data = parse_excel_file(full_path)
        
        # Create a temporary fixture file
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp_file:
            fixture_path = temp_file.name
        
        # Generate fixture from Excel data
        generated_path = generate_fixture_from_excel_data(excel_data, fixture_path)
        
        # Check if fixture file exists
        self.assertTrue(os.path.exists(generated_path))
        
        # Read the fixture file to check its contents
        with open(generated_path, 'r', encoding='utf-8') as f:
            fixture_data = json.load(f)
        
        # Check if fixture data is valid
        self.assertEqual(len(fixture_data), 6)  # 2 teachers + 2 courses + 2 timeslots
        
        # Check models in fixture
        models = [item['model'] for item in fixture_data]
        self.assertIn('dance.teacher', models)
        self.assertIn('dance.course', models)
        self.assertIn('dance.timeslot', models)
        
        # Clean up files
        os.remove(full_path)
        os.remove(fixture_path)
    
    def test_update_database_from_fixture(self):
        """Test updating database from fixture"""
        # First export data to create a valid Excel file
        excel_path = export_to_excel()
        full_path = os.path.join(settings.BASE_DIR, excel_path)
        
        # Parse the Excel file
        excel_data = parse_excel_file(full_path)
        
        # Modify the data to test update
        excel_data['teachers'][0]['name'] = 'Modified Teacher Name'
        
        # Create a temporary fixture file
        fixture_path = os.path.join(settings.BASE_DIR, 'dance', 'fixtures', 'test_fixture.json')
        
        # Generate fixture from Excel data
        generate_fixture_from_excel_data(excel_data, fixture_path)
        
        # Update database from fixture
        result = update_database_from_fixture(fixture_path)
        
        # Check if update was successful
        self.assertTrue(result)
        
        # Check if data was updated
        updated_teacher = Teacher.objects.get(id=self.teacher1.id)
        self.assertEqual(updated_teacher.name, 'Modified Teacher Name')
        
        # Clean up files
        os.remove(full_path)
        os.remove(fixture_path)
    
    def test_excel_export_view(self):
        """Test Excel export view"""
        # Login required for this view
        self.client.force_login(user=self._create_user())
        
        # Request the export view
        response = self.client.get(reverse('dance:excel_export'))
        
        # Check if response is a file response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    def test_excel_import_view(self):
        """Test Excel import view"""
        # First export data to create a valid Excel file
        excel_path = export_to_excel()
        full_path = os.path.join(settings.BASE_DIR, excel_path)
        
        # Create a modified excel file
        xl = pd.ExcelFile(full_path)
        df_teachers = pd.read_excel(xl, sheet_name='Teachers')
        df_courses = pd.read_excel(xl, sheet_name='Courses')
        df_timeslots = pd.read_excel(xl, sheet_name='TimeSlots')
        
        # Modify a teacher name
        df_teachers.loc[0, 'name'] = 'Modified Import Teacher'
        
        # Save modified excel
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            modified_path = temp_file.name
            
        with pd.ExcelWriter(modified_path, engine='openpyxl') as writer:
            df_teachers.to_excel(writer, sheet_name='Teachers', index=False)
            df_courses.to_excel(writer, sheet_name='Courses', index=False)
            df_timeslots.to_excel(writer, sheet_name='TimeSlots', index=False)
        
        # Login required for this view
        self.client.force_login(user=self._create_user())
        
        # Read the file to upload
        with open(modified_path, 'rb') as file:
            file_content = file.read()
        
        # Create uploaded file
        uploaded_file = SimpleUploadedFile("test_import.xlsx", file_content, 
                                          content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # Submit the import form
        response = self.client.post(reverse('dance:excel_import'), {'excel_file': uploaded_file})
        
        # Check redirect
        self.assertEqual(response.status_code, 302)
        
        # Check if data was updated
        updated_teacher = Teacher.objects.get(id=self.teacher1.id)
        self.assertEqual(updated_teacher.name, 'Modified Import Teacher')
        
        # Clean up files
        os.remove(full_path)
        os.remove(modified_path)
    
    def _create_user(self):
        """Create a test user"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            is_staff=True
        )
