from django.contrib import admin
from .models import Student, StudentAcademicInfo

class StudentAcademicInfoInline(admin.StackedInline):
    model = StudentAcademicInfo
    can_delete = False

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'phone', 'admission_date', 'is_active')
    list_filter = ('is_active', 'admission_date')
    search_fields = ('student_id', 'full_name', 'email')
    inlines = [StudentAcademicInfoInline]
    fieldsets = (
        (None, {
            'fields': ('student_id', 'full_name', 'date_of_birth', 'gender')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
