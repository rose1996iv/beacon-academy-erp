from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Student, StudentAcademicInfo
from .forms import StudentForm, StudentAcademicInfoForm

@login_required
@permission_required('students.view_student')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
@permission_required('students.add_student')
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        academic_form = StudentAcademicInfoForm(request.POST)
        if form.is_valid() and academic_form.is_valid():
            student = form.save()
            academic_info = academic_form.save(commit=False)
            academic_info.student = student
            academic_info.save()
            messages.success(request, 'Student created successfully.')
            return redirect('students:list')
    else:
        form = StudentForm()
        academic_form = StudentAcademicInfoForm()
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'academic_form': academic_form,
        'title': 'Add New Student'
    })

@login_required
@permission_required('students.change_student')
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    academic_info = student.academic_info.first()
    if not academic_info:
        academic_info = StudentAcademicInfo(student=student)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        academic_form = StudentAcademicInfoForm(request.POST, instance=academic_info)
        if form.is_valid() and academic_form.is_valid():
            # Delete old photo if a new one is uploaded
            if 'profile_photo' in request.FILES and student.profile_photo:
                student.profile_photo.delete(save=False)
            form.save()
            academic_form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('students:list')
    else:
        form = StudentForm(instance=student)
        academic_form = StudentAcademicInfoForm(instance=academic_info)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'academic_form': academic_form,
        'title': 'Edit Student',
        'student': student
    })

@login_required
@permission_required('students.delete_student')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('students:list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

@login_required
@permission_required('students.view_student')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    academic_info = student.studentacademicinfo_set.first()
    return render(request, 'students/student_detail.html', {
        'student': student,
        'academic_info': academic_info,
    })
