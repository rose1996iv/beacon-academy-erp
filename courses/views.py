from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Prefetch
from .models import Course, CourseSchedule
from .forms import CourseForm, CourseScheduleForm
from instructors.models import CourseInstructor

@login_required
@permission_required('courses.view_course')
def course_list(request):
    courses = Course.objects.select_related().all().order_by('code')
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
@permission_required('courses.add_course')
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        schedule_form = CourseScheduleForm(request.POST)
        if form.is_valid():
            course = form.save()
            schedule = schedule_form.save(commit=False)
            schedule.course = course
            if schedule_form.is_valid():
                schedule.save()
                messages.success(request, 'Course created successfully.')
                return redirect('courses:course_list')
            else:
                course.delete()
                messages.error(request, 'Invalid schedule details.')
    else:
        form = CourseForm()
        schedule_form = CourseScheduleForm()
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'schedule_form': schedule_form,
        'title': 'Add New Course'
    })

@login_required
@permission_required('courses.change_course')
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    schedule = course.courseschedule_set.first()
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        schedule_form = CourseScheduleForm(request.POST, instance=schedule)
        if form.is_valid() and schedule_form.is_valid():
            form.save()
            schedule_form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
        schedule_form = CourseScheduleForm(instance=schedule)
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'schedule_form': schedule_form,
        'title': 'Update Course'
    })

@login_required
@permission_required('courses.delete_course')
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

@login_required
@permission_required('courses.view_course')
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    schedule = course.courseschedule_set.first()
    instructors = CourseInstructor.objects.filter(
        course=course,
        instructor__is_active=True
    ).select_related('instructor__user')
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'schedule': schedule,
        'instructors': instructors
    })
