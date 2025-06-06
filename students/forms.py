from django import forms
from .models import Student, StudentAcademicInfo

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',
            'full_name',
            'date_of_birth',
            'gender',
            'email',
            'phone',
            'address',
            'profile_photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            # Check file size - limit to 5MB
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size must be less than 5MB.")
            # Check file type
            if not photo.content_type.startswith('image'):
                raise forms.ValidationError("File must be an image.")
        return photo

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
