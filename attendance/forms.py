from django import forms
from django.core.exceptions import ValidationError
from .models import AttendanceRecord

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'course', 'date', 'status', 'minutes_late', 'notes']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'minutes_late': forms.NumberInput(attrs={
                'placeholder': 'Minutes late (if applicable)',
                'class': 'form-control',
                'min': 1,
                'max': 180
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Add any additional notes here',
                'class': 'form-control',
                'rows': 3
            })
        }
        help_texts = {
            'student': 'Select the student',
            'course': 'Select the course',
            'date': 'Date of attendance',
            'status': 'Present, Absent, Late, or Excused',
            'minutes_late': 'If student was late, enter minutes (max 180)',
            'notes': 'Any additional information about the attendance'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        minutes_late = cleaned_data.get('minutes_late')
        
        if status == 'L' and not minutes_late:
            raise ValidationError("Minutes late is required when status is Late.")
        elif status != 'L' and minutes_late:
            cleaned_data['minutes_late'] = None
        
        return cleaned_data

class BulkAttendanceForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select course'
        }),
        help_text='Select the course to mark attendance for'
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        help_text='Date for marking attendance'
    )
    
    def __init__(self, *args, **kwargs):
        instructor = kwargs.pop('instructor', None)
        super().__init__(*args, **kwargs)
        if instructor:
            self.fields['course'].queryset = instructor.courseinstructor_set.filter(
                is_active=True
            ).select_related('course')

class AttendanceReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        help_text='Start date for the report period'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        help_text='End date for the report period'
    )
    course = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select course (optional)'
        }),
        help_text='Filter by specific course (optional)'
    )
    student = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select student (optional)'
        }),
        help_text='Filter by specific student (optional)'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from courses.models import Course
        from students.models import Student
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise ValidationError("End date must be after start date.")
