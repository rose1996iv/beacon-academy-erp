from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import AttendanceRecord
from courses.models import Course, CourseEnrollment
from students.models import Student
from django.http import JsonResponse

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
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        course = get_object_or_404(Course, pk=course_id)
        
        # Get all active enrollments for the course
        enrollments = CourseEnrollment.objects.filter(course=course, is_active=True)
        
        for enrollment in enrollments:
            student = enrollment.student
            status = request.POST.get(f'status_{student.id}')
            minutes_late = request.POST.get(f'minutes_late_{student.id}')
            notes = request.POST.get(f'notes_{student.id}')
            
            if status:  # Only create/update record if status is provided
                # Create or update attendance record
                AttendanceRecord.objects.update_or_create(
                    student=student,
                    course=course,
                    date=date,
                    defaults={
                        'status': status,
                        'minutes_late': minutes_late if minutes_late and status == 'L' else None,
                        'notes': notes,
                        'marked_by': request.user.instructor if hasattr(request.user, 'instructor') else None
                    }
                )
        
        messages.success(request, 'Attendance marked successfully.')
        return redirect('attendance:list')

    courses = Course.objects.filter(is_active=True)
    return render(request, 'attendance/mark_attendance.html', {
        'courses': courses,
        'today': timezone.now().date()
    })

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

@login_required
def attendance_edit(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        minutes_late = request.POST.get('minutes_late')
        notes = request.POST.get('notes')
        
        record.status = status
        record.minutes_late = minutes_late if minutes_late and status == 'L' else None
        record.notes = notes
        record.save()
        
        messages.success(request, 'Attendance record updated successfully.')
        return redirect('attendance:list')
        
    return render(request, 'attendance/attendance_edit.html', {
        'record': record,
        'statuses': AttendanceRecord.ATTENDANCE_STATUS
    })

@login_required
def attendance_delete(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('attendance:list')
        
    return render(request, 'attendance/attendance_confirm_delete.html', {'record': record})

@login_required
def get_enrolled_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrolled_students = course.courseenrollment_set.filter(is_active=True).select_related('student')
    
    students_data = [{
        'id': enrollment.student.id,
        'student_id': enrollment.student.student_id,
        'full_name': enrollment.student.full_name
    } for enrollment in enrolled_students]
    
    return JsonResponse({'students': students_data})
