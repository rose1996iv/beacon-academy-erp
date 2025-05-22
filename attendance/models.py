from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class AttendanceRecord(models.Model):
    ATTENDANCE_STATUS = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused')
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS)
    marked_by = models.ForeignKey('instructors.Instructor', on_delete=models.SET_NULL, null=True)
    time_marked = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    # For late attendance
    minutes_late = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MaxValueValidator(180)]  # Maximum 3 hours late
    )

    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date', 'course']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['student', 'date']),
        ]

    def __str__(self):
        return f"{self.student} - {self.course} ({self.date})"

    def save(self, *args, **kwargs):
        if self.status != 'L':
            self.minutes_late = None
        super().save(*args, **kwargs)
