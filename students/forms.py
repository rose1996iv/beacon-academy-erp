from django import forms
from .models import Student, StudentAcademicInfo

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'date_of_birth', 'gender', 'address', 'phone', 'email']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'placeholder': 'Enter student ID (e.g., 2023001)',
                'class': 'form-control'
            }),
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter full name',
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter complete address',
                'class': 'form-control',
                'rows': 3
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter phone number',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email address',
                'class': 'form-control'
            })
        }
        help_texts = {
            'student_id': 'A unique identifier for the student',
            'full_name': 'Enter the complete name as in official documents',
            'phone': 'Enter a valid phone number',
            'email': 'Enter a valid email address - this will be used for login'
        }

class StudentAcademicInfoForm(forms.ModelForm):
    class Meta:
        model = StudentAcademicInfo
        fields = ['current_semester', 'batch', 'department', 'cgpa']
        widgets = {
            'current_semester': forms.NumberInput(attrs={
                'placeholder': 'Enter current semester (1-8)',
                'class': 'form-control',
                'min': 1,
                'max': 8
            }),
            'batch': forms.TextInput(attrs={
                'placeholder': 'Enter batch (e.g., 2023)',
                'class': 'form-control'
            }),
            'department': forms.TextInput(attrs={
                'placeholder': 'Enter department name',
                'class': 'form-control'
            }),
            'cgpa': forms.NumberInput(attrs={
                'placeholder': 'Enter CGPA (0.00-4.00)',
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'max': 4
            })
        }
        help_texts = {
            'current_semester': 'Current semester of study (1-8)',
            'batch': 'Year of admission batch',
            'department': 'Academic department name',
            'cgpa': 'Cumulative Grade Point Average (0.00-4.00)'
        }
