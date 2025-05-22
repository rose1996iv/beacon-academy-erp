from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import AttendanceRecord
from courses.models import Course
from students.models import Student

@login_required
def attendance_list(request):
    today = timezone.now().date()
    attendance_records = AttendanceRecord.objects.filter(date=today)
    return render(request, 'attendance/attendance_list.html', {
        'attendance_records': attendance_records,
        'date': today
    })

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        # Form handling will be implemented later
        pass
    courses = Course.objects.filter(is_active=True)
    return render(request, 'attendance/mark_attendance.html', {'courses': courses})

@login_required
def attendance_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    course_id = request.GET.get('course_id')
    
    records = AttendanceRecord.objects.all()
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)
    if course_id:
        records = records.filter(course_id=course_id)
    
    return render(request, 'attendance/attendance_report.html', {
        'records': records,
        'courses': Course.objects.filter(is_active=True)
    })

@login_required
def course_attendance(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    date = request.GET.get('date', timezone.now().date())
    records = AttendanceRecord.objects.filter(course=course, date=date)
    
    return render(request, 'attendance/course_attendance.html', {
        'course': course,
        'records': records,
        'date': date
    })

@login_required
def student_attendance(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    records = AttendanceRecord.objects.filter(student=student)
    
    return render(request, 'attendance/student_attendance.html', {
        'student': student,
        'records': records
    })
