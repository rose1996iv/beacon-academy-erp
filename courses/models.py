from django.db import models
from django.core.exceptions import ValidationError

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField()
    semester = models.IntegerField()
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_choices = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    ]
    day = models.CharField(max_length=3, choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)

    class Meta:
        unique_together = ['course', 'day', 'start_time']

    def __str__(self):
        return f"{self.course.code} - {self.get_day_display()} ({self.start_time} - {self.end_time})"

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({
                'end_time': 'End time must be after start time'
            })
        
        # Check for schedule conflicts
        if self.pk:  # Only check if this is an existing schedule
            conflicts = CourseSchedule.objects.exclude(pk=self.pk).filter(
                course=self.course,
                day=self.day,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
        else:
            conflicts = CourseSchedule.objects.filter(
                course=self.course,
                day=self.day,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )
        
        if conflicts.exists():
            raise ValidationError(
                'This schedule conflicts with another schedule for this course'
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
