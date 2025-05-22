from django.contrib import admin
from .models import Course, CourseSchedule

class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'semester', 'department', 'is_active')
    list_filter = ('department', 'semester', 'is_active')
    search_fields = ('code', 'name', 'description')
    inlines = [CourseScheduleInline]
