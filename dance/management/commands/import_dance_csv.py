# Command to import dance course data from CSV to a JSON fixture

import csv
import json
import re
from datetime import time
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import os

# Helper function to parse time string like "HH:MM"
def parse_time(time_str):
    try:
        hour, minute = map(int, time_str.split(':'))
        return time(hour, minute)
    except ValueError:
        return None

# Helper function to parse day/time strings like "Montag (15:30-17:00)" or "Dienstag (15:30-17:00), Freitag (15:30-17:00)"
def parse_day_time_string(dt_string):
    slots = []
    # Regex to find Day (HH:MM-HH:MM) patterns
    pattern = re.compile(r"(\w+)\s*\((\d{1,2}:\d{2})-(\d{1,2}:\d{2})\)")
    matches = pattern.findall(dt_string)
    for match in matches:
        day, start_str, end_str = match
        start_t = parse_time(start_str)
        end_t = parse_time(end_str)
        if start_t and end_t:
            slots.append({
                'day': day.strip(),
                'start_time': start_t,
                'end_time': end_t
            })
    return slots

class Command(BaseCommand):
    help = 'Imports dance course data from a CSV file and outputs a JSON fixture.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='Path to the CSV file')
        parser.add_argument('--output', type=str, default='dance_fixture.json', help='Output JSON fixture file path')
        # Add argument for studio mapping if needed later

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        output_file_path = options['output']

        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
            return

        teachers = {}
        courses = {}
        timeslots = []
        objects_for_fixture = []
        teacher_pk = 1
        course_pk = 1
        timeslot_pk = 1

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                for row in reader:
                    teacher_name = row.get('Lehrer/in', '').strip()
                    teacher_email = row.get('Kontakt', '').strip().lower() # Use email as unique ID
                    course_name = row.get('Kursname', '').strip()
                    age_group = row.get('Altersgruppe', '').strip()
                    description = row.get('Beschreibung', '').strip()
                    day_time_str = row.get('Tag(e) und Zeit(en)', '').strip()

                    if not teacher_name or not teacher_email or not course_name or not day_time_str:
                        self.stdout.write(self.style.WARNING(f"Skipping row due to missing data: {row}"))
                        continue

                    # --- Create/Get Teacher --- 
                    current_teacher_pk = None
                    if teacher_email not in teachers:
                        current_teacher_pk = teacher_pk
                        teacher_data = {
                            "model": "dance.teacher",
                            "pk": current_teacher_pk,
                            "fields": {
                                "name": teacher_name,
                                "email": teacher_email
                            }
                        }
                        objects_for_fixture.append(teacher_data)
                        teachers[teacher_email] = current_teacher_pk
                        teacher_pk += 1
                    else:
                        current_teacher_pk = teachers[teacher_email]

                    # --- Create Course --- 
                    # Assuming course name + teacher is unique enough for this import
                    course_key = (course_name, current_teacher_pk)
                    current_course_pk = None
                    if course_key not in courses:
                        current_course_pk = course_pk
                        course_data = {
                            "model": "dance.course",
                            "pk": current_course_pk,
                            "fields": {
                                "name": course_name,
                                "teacher": current_teacher_pk,
                                "age_group": age_group,
                                "description": description
                            }
                        }
                        objects_for_fixture.append(course_data)
                        courses[course_key] = current_course_pk
                        course_pk += 1
                    else:
                        current_course_pk = courses[course_key]

                    # --- Create TimeSlots --- 
                    parsed_slots = parse_day_time_string(day_time_str)
                    if not parsed_slots:
                         self.stdout.write(self.style.WARNING(f"Could not parse timeslots for course '{course_name}': {day_time_str}"))
                         continue
                         
                    for slot in parsed_slots:
                        # Add Studio logic here if mapping is provided
                        studio_value = None # Placeholder

                        timeslot_data = {
                            "model": "dance.timeslot",
                            "pk": timeslot_pk,
                            "fields": {
                                "course": current_course_pk,
                                "day": slot['day'],
                                "start_time": slot['start_time'].strftime('%H:%M:%S'), # Format for JSON
                                "end_time": slot['end_time'].strftime('%H:%M:%S'), # Format for JSON
                                "studio": studio_value
                            }
                        }
                        objects_for_fixture.append(timeslot_data)
                        timeslot_pk += 1
                        
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
            return
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
            return
            
        # Write the fixture file
        try:
            with open(output_file_path, 'w', encoding='utf-8') as outfile:
                json.dump(objects_for_fixture, outfile, cls=DjangoJSONEncoder, indent=4, ensure_ascii=False)
            self.stdout.write(self.style.SUCCESS(f'Successfully created fixture file: {output_file_path}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to write fixture file: {e}"))

