from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'minutes_late', 'marked_by')
    list_filter = ('status', 'date', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__name', 'notes')
    date_hierarchy = 'date'
    raw_id_fields = ('student', 'course', 'marked_by')
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('student', 'course', 'date', 'status')
        }),
        ('Late Details', {
            'fields': ('minutes_late',),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('marked_by', 'notes')
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('time_marked',)
        return ()
