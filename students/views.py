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
        form = StudentForm(request.POST)
        academic_form = StudentAcademicInfoForm(request.POST)
        if form.is_valid() and academic_form.is_valid():
            student = form.save()
            academic_info = academic_form.save(commit=False)
            academic_info.student = student
            academic_info.save()
            messages.success(request, 'Student created successfully.')
            return redirect('student_list')
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
    academic_info = student.studentacademicinfo_set.first()
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        academic_form = StudentAcademicInfoForm(request.POST, instance=academic_info)
        if form.is_valid() and academic_form.is_valid():
            form.save()
            academic_form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
        academic_form = StudentAcademicInfoForm(instance=academic_info)
    
    return render(request, 'students/student_form.html', {
        'form': form,
        'academic_form': academic_form,
        'title': 'Update Student'
    })

@login_required
@permission_required('students.delete_student')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
