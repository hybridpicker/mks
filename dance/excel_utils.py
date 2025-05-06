import json
import os
import pandas as pd
from datetime import datetime
from django.conf import settings
from django.core.management import call_command
from .models import Teacher, Course, TimeSlot

def export_to_excel():
    """
    Exports all dance class data to an Excel file.
    """
    # Export teachers
    teachers = Teacher.objects.all().order_by('id')
    teachers_data = []
    
    for teacher in teachers:
        teachers_data.append({
            'id': teacher.id,
            'name': teacher.name,
            'email': teacher.email
        })
    
    # Export courses
    courses = Course.objects.all().order_by('id')
    courses_data = []
    
    for course in courses:
        courses_data.append({
            'id': course.id,
            'name': course.name,
            'teacher_id': course.teacher_id,
            'teacher_name': course.teacher.name,
            'age_group': course.age_group,
            'description': course.description
        })
    
    # Export time slots
    timeslots = TimeSlot.objects.all().order_by('id')
    timeslots_data = []
    
    for timeslot in timeslots:
        timeslots_data.append({
            'id': timeslot.id,
            'course_id': timeslot.course_id,
            'course_name': timeslot.course.name,
            'day': timeslot.day,
            'start_time': timeslot.start_time.strftime('%H:%M:%S'),
            'end_time': timeslot.end_time.strftime('%H:%M:%S'),
            'studio': timeslot.studio if timeslot.studio else None,
            'location': timeslot.location if timeslot.location else None
        })
    
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'dance_classes_export_{timestamp}.xlsx'
    file_path = os.path.join(settings.MEDIA_ROOT, 'excel_exports', file_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Convert data to DataFrames
    df_teachers = pd.DataFrame(teachers_data)
    df_courses = pd.DataFrame(courses_data)
    df_timeslots = pd.DataFrame(timeslots_data)
    
    # Create the Excel workbook with multiple sheets using context manager
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # Save DataFrames to separate sheets with more explicit formatting
        if not df_teachers.empty:
            df_teachers.to_excel(writer, sheet_name='Teachers', index=False)
            
        if not df_courses.empty:
            df_courses.to_excel(writer, sheet_name='Courses', index=False)
            
        if not df_timeslots.empty:
            df_timeslots.to_excel(writer, sheet_name='TimeSlots', index=False)
    
    # Return the relative file path for download
    relative_path = os.path.join('media', 'excel_exports', file_name)
    return relative_path

def parse_excel_file(file_path):
    """
    Parses an uploaded Excel file and returns the data.
    """
    # Read Excel file
    xl = pd.ExcelFile(file_path)
    
    # Check if all required sheets are present
    required_sheets = ['Teachers', 'Courses', 'TimeSlots']
    for sheet in required_sheets:
        if sheet not in xl.sheet_names:
            raise ValueError(f"Sheet '{sheet}' is missing in the Excel file.")
    
    # Read data from sheets
    df_teachers = pd.read_excel(xl, sheet_name='Teachers')
    df_courses = pd.read_excel(xl, sheet_name='Courses')
    df_timeslots = pd.read_excel(xl, sheet_name='TimeSlots')
    
    # Ensure all required columns are present
    # Teachers
    required_teacher_cols = ['id', 'name', 'email']
    missing_teacher_cols = [col for col in required_teacher_cols if col not in df_teachers.columns]
    if missing_teacher_cols:
        raise ValueError(f"Missing required columns in Teachers sheet: {', '.join(missing_teacher_cols)}")
    
    # Courses
    required_course_cols = ['id', 'name', 'teacher_id', 'age_group', 'description']
    missing_course_cols = [col for col in required_course_cols if col not in df_courses.columns]
    if missing_course_cols:
        raise ValueError(f"Missing required columns in Courses sheet: {', '.join(missing_course_cols)}")
    
    # TimeSlots
    required_timeslot_cols = ['id', 'course_id', 'day', 'start_time', 'end_time']
    missing_timeslot_cols = [col for col in required_timeslot_cols if col not in df_timeslots.columns]
    if missing_timeslot_cols:
        raise ValueError(f"Missing required columns in TimeSlots sheet: {', '.join(missing_timeslot_cols)}")
    
    # Convert to lists of dictionaries for easier processing
    teachers_data = df_teachers.to_dict('records')
    courses_data = df_courses.to_dict('records')
    timeslots_data = df_timeslots.to_dict('records')
    
    return {
        'teachers': teachers_data,
        'courses': courses_data,
        'timeslots': timeslots_data
    }

def generate_fixture_from_excel_data(excel_data, fixture_path):
    """
    Generates a fixture file from Excel data.
    """
    fixture_data = []
    
    # Add teachers to fixture
    for teacher in excel_data['teachers']:
        fixture_data.append({
            'model': 'dance.teacher',
            'pk': int(teacher['id']),
            'fields': {
                'name': str(teacher['name']),
                'email': str(teacher['email'])
            }
        })
    
    # Add courses to fixture
    for course in excel_data['courses']:
        # Ensure teacher_id is an integer
        teacher_id = int(course['teacher_id'])
        
        fixture_data.append({
            'model': 'dance.course',
            'pk': int(course['id']),
            'fields': {
                'name': str(course['name']),
                'teacher': teacher_id,
                'age_group': str(course['age_group']),
                'description': str(course['description']) if pd.notna(course['description']) else ''
            }
        })
    
    # Add time slots to fixture
    for timeslot in excel_data['timeslots']:
        # Handle different time formats
        start_time = timeslot['start_time']
        end_time = timeslot['end_time']
        
        # Convert to string if not already
        if not isinstance(start_time, str):
            if pd.isna(start_time):
                raise ValueError(f"Missing start_time for timeslot {timeslot['id']}")
            # If pandas timestamp or datetime
            if hasattr(start_time, 'strftime'):
                start_time = start_time.strftime('%H:%M:%S')
            else:
                start_time = str(start_time)
                
        if not isinstance(end_time, str):
            if pd.isna(end_time):
                raise ValueError(f"Missing end_time for timeslot {timeslot['id']}")
            # If pandas timestamp or datetime
            if hasattr(end_time, 'strftime'):
                end_time = end_time.strftime('%H:%M:%S')
            else:
                end_time = str(end_time)
        
        # Ensure times are in HH:MM:SS format
        if len(start_time) == 5:  # Format is HH:MM
            start_time += ':00'
        if len(end_time) == 5:  # Format is HH:MM
            end_time += ':00'
        
        # Process studio and location fields
        studio = timeslot.get('studio')
        location = timeslot.get('location')
        
        # Convert to None if empty or NaN
        studio = None if pd.isna(studio) or studio == '' or studio == 'None' else str(studio)
        location = None if pd.isna(location) or location == '' or location == 'None' else str(location)
        
        fixture_data.append({
            'model': 'dance.timeslot',
            'pk': int(timeslot['id']),
            'fields': {
                'course': int(timeslot['course_id']),
                'day': str(timeslot['day']),
                'start_time': start_time,
                'end_time': end_time,
                'studio': studio,
                'location': location
            }
        })
    
    # Write fixture file with proper formatting
    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, ensure_ascii=False, indent=2)
    
    return fixture_path

def update_database_from_fixture(fixture_path):
    """
    Updates the database with data from the fixture file.
    """
    try:
        # Clear existing data to avoid conflicts
        # Note: Due to CASCADE, deleting teachers will delete all related courses and timeslots
        Teacher.objects.all().delete()
        
        # Load fixture file into database
        call_command('loaddata', fixture_path)
        
        # Return success
        return True
    except Exception as e:
        raise Exception(f"Failed to update database from fixture: {str(e)}")

