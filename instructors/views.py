from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Instructor, CourseInstructor
from .forms import InstructorForm

@login_required
def instructor_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'instructors/instructor_list.html', {'instructors': instructors})

@login_required
def instructor_detail(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    courses = instructor.get_active_courses()
    return render(request, 'instructors/instructor_detail.html', {
        'instructor': instructor,
        'courses': courses
    })

@login_required
@permission_required('instructors.add_instructor')
def instructor_add(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            instructor = form.save()
            messages.success(request, 'Instructor added successfully.')
            return redirect('instructors:detail', pk=instructor.pk)
    else:
        form = InstructorForm()
    return render(request, 'instructors/instructor_form.html', {
        'form': form,
        'title': 'Add New Instructor'
    })

@login_required
@permission_required('instructors.change_instructor')
def instructor_edit(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Instructor information updated successfully.')
            return redirect('instructors:detail', pk=instructor.pk)
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'instructors/instructor_form.html', {
        'form': form,
        'instructor': instructor,
        'title': 'Edit Instructor'
    })

@login_required
@permission_required('instructors.delete_instructor')
def instructor_delete(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    if request.method == 'POST':
        instructor.is_active = False
        instructor.save()
        messages.success(request, 'Instructor has been deactivated successfully.')
        return redirect('instructors:list')
    return render(request, 'instructors/instructor_confirm_delete.html', {
        'instructor': instructor
    })

@login_required
def instructor_courses(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    assignments = CourseInstructor.objects.filter(instructor=instructor).select_related('course')
    return render(request, 'instructors/instructor_courses.html', {
        'instructor': instructor,
        'assignments': assignments
    })
