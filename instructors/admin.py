from django.contrib import admin
from .models import Instructor, CourseInstructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'specialization', 'phone', 'teaching_experience', 'is_active')
    list_filter = ('is_active', 'date_joined', 'specialization')
    search_fields = ('user__first_name', 'user__last_name', 'specialization', 'phone')
    date_hierarchy = 'date_joined'
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'qualifications', 'teaching_experience', 'bio')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    raw_id_fields = ('user',)

@admin.register(CourseInstructor)
class CourseInstructorAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'course', 'date_assigned', 'is_primary')
    list_filter = ('is_primary', 'date_assigned')
    search_fields = ('instructor__user__first_name', 'instructor__user__last_name', 'course__name')
    date_hierarchy = 'date_assigned'
    raw_id_fields = ('instructor', 'course')
