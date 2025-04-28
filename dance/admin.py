from django.contrib import admin
from .models import Teacher, Course, TimeSlot

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1 # Show one extra empty form for adding timeslots
    fields = ('day', 'start_time', 'end_time', 'studio')
    ordering = ('day', 'start_time')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'age_group')
    list_filter = ('teacher', 'age_group')
    search_fields = ('name', 'description', 'teacher__name')
    inlines = [TimeSlotInline] # Add timeslots directly within the course admin

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time', 'studio', 'location')
    list_filter = ('day', 'studio', 'location', 'course__teacher')
    search_fields = ('course__name', 'studio', 'location')
    # Consider making course selectable via raw_id_fields if many courses exist
    # raw_id_fields = ('course',) 
