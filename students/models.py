from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.user and self.email:
            # Create user account if it doesn't exist
            username = self.email.split('@')[0]
            # Add number if username exists
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{self.email.split('@')[0]}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=self.email,
                first_name=self.full_name.split()[0],
                last_name=' '.join(self.full_name.split()[1:]) if len(self.full_name.split()) > 1 else '',
            )
            # Set a default password as student ID
            user.set_password(self.student_id)
            user.save()
            self.user = user
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"

class StudentAcademicInfo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    current_semester = models.IntegerField()
    batch = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - Semester {self.current_semester}"
