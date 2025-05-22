from django import forms
from django.contrib.auth.models import User
from .models import Instructor, CourseInstructor

class InstructorForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter first name',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter last name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email address',
            'class': 'form-control'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username for login',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'form-control'
        }),
        required=False,
        help_text='Leave empty if not changing password'
    )

    class Meta:
        model = Instructor
        fields = [
            'phone', 'address', 'specialization', 'qualifications',
            'teaching_experience', 'bio', 'emergency_contact_name',
            'emergency_contact_phone'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter phone number (e.g., +1234567890)',
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter complete address',
                'class': 'form-control',
                'rows': 3
            }),
            'specialization': forms.TextInput(attrs={
                'placeholder': 'Enter area of specialization',
                'class': 'form-control'
            }),
            'qualifications': forms.Textarea(attrs={
                'placeholder': 'Enter academic qualifications',
                'class': 'form-control',
                'rows': 3
            }),
            'teaching_experience': forms.NumberInput(attrs={
                'placeholder': 'Years of teaching experience',
                'class': 'form-control',
                'min': 0
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Enter professional biography',
                'class': 'form-control',
                'rows': 4
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'placeholder': 'Emergency contact person name',
                'class': 'form-control'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'placeholder': 'Emergency contact phone number',
                'class': 'form-control'
            })
        }
        help_texts = {
            'phone': 'Enter phone number in international format (e.g., +1234567890)',
            'specialization': 'Primary area of expertise',
            'qualifications': 'List all relevant academic qualifications',
            'teaching_experience': 'Total years of teaching experience',
            'emergency_contact_name': 'Name of person to contact in emergencies',
            'emergency_contact_phone': 'Phone number for emergency contact'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['password'].required = False
        else:
            self.fields['password'].required = True

    def save(self, commit=True):
        instructor = super().save(commit=False)
        if not instructor.pk:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            instructor.user = user
        else:
            instructor.user.first_name = self.cleaned_data['first_name']
            instructor.user.last_name = self.cleaned_data['last_name']
            instructor.user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                instructor.user.set_password(self.cleaned_data['password'])
            instructor.user.save()
        
        if commit:
            instructor.save()
        return instructor

class CourseInstructorForm(forms.ModelForm):
    class Meta:
        model = CourseInstructor
        fields = ['course', 'is_primary', 'notes']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Enter any additional notes',
                'class': 'form-control',
                'rows': 3
            })
        }
        help_texts = {
            'is_primary': 'Check if this is the primary instructor for the course',
            'notes': 'Any additional information about the instructor\'s role in this course'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = self.fields['course'].queryset.filter(is_active=True)
