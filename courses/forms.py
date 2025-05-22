from django import forms
from .models import Course, CourseSchedule

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credits', 'semester', 'department', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={
                'placeholder': 'Enter course code (e.g., CS101)',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter course name',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter course description',
                'class': 'form-control',
                'rows': 3
            }),
            'credits': forms.NumberInput(attrs={
                'placeholder': 'Number of credits',
                'class': 'form-control',
                'min': 1,
                'max': 6
            }),
            'semester': forms.NumberInput(attrs={
                'placeholder': 'Enter semester number (1-8)',
                'class': 'form-control',
                'min': 1,
                'max': 8
            }),
            'department': forms.TextInput(attrs={
                'placeholder': 'Enter department name',
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'code': 'A unique identifier for the course (e.g., CS101)',
            'credits': 'Number of credit hours (1-6)',
            'semester': 'The semester in which this course is typically offered (1-8)',
            'department': 'The department offering this course',
            'is_active': 'Whether this course is currently being offered'
        }

class CourseScheduleForm(forms.ModelForm):
    class Meta:
        model = CourseSchedule
        fields = ['day', 'start_time', 'end_time', 'room']
        widgets = {
            'day': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'room': forms.TextInput(attrs={
                'placeholder': 'Enter room number/name',
                'class': 'form-control'
            })
        }
        help_texts = {
            'day': 'Select the day of the week',
            'start_time': 'Class start time',
            'end_time': 'Class end time',
            'room': 'Room number or name where the class is held'
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('End time must be after start time')
