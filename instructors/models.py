from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Professional information
    specialization = models.CharField(max_length=100)
    qualifications = models.TextField()
    teaching_experience = models.PositiveIntegerField(help_text="Years of teaching experience")
    bio = models.TextField()
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(validators=[phone_regex], max_length=17)
    
    courses = models.ManyToManyField('courses.Course', through='CourseInstructor')

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialization})"

    def get_active_courses(self):
        return self.courses.filter(is_active=True)

    def get_full_name(self):
        return self.user.get_full_name()

class CourseInstructor(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['instructor', 'course']
        ordering = ['-date_assigned']

    def __str__(self):
        return f"{self.instructor} - {self.course}"
