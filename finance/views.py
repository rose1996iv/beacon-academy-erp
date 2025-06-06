from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum
from .models import Fee, Payment, Scholarship
from .forms import FeeForm, PaymentForm, ScholarshipForm
from students.models import Student

@login_required
@permission_required('finance.view_fee')
def fee_list(request):
    fees = Fee.objects.all()
    return render(request, 'finance/fee_list.html', {'fees': fees})

@login_required
@permission_required('finance.add_fee')
def fee_create(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure created successfully.')
            return redirect('finance:fee_list')
    else:
        form = FeeForm()
    return render(request, 'finance/fee_form.html', {'form': form})

@login_required
@permission_required('finance.change_fee')
def fee_edit(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure updated successfully.')
            return redirect('finance:fee_list')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'finance/fee_form.html', {'form': form, 'fee': fee})

@login_required
@permission_required('finance.delete_fee')
def fee_delete(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        fee.delete()
        messages.success(request, 'Fee structure deleted successfully.')
        return redirect('finance:fee_list')
    return render(request, 'finance/fee_confirm_delete.html', {'fee': fee})

@login_required
@permission_required('finance.view_payment')
def payment_list(request):
    payments = Payment.objects.all().order_by('-payment_date')
    students = Student.objects.filter(is_active=True)
    fees = Fee.objects.filter(is_active=True)
    
    # Filter by student
    student_id = request.GET.get('student')
    if student_id:
        payments = payments.filter(student_id=student_id)
    
    # Filter by fee
    fee_id = request.GET.get('fee')
    if fee_id:
        payments = payments.filter(fee_id=fee_id)
        
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        payments = payments.filter(payment_date__gte=start_date)
    if end_date:
        payments = payments.filter(payment_date__lte=end_date)
    
    return render(request, 'finance/payment_list.html', {
        'payments': payments,
        'students': students,
        'fees': fees
    })

@login_required
@permission_required('finance.add_payment')
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f'Payment recorded successfully. Receipt: {payment.receipt_number}')
            return redirect('finance:payment_list')
    else:
        form = PaymentForm()
    return render(request, 'finance/payment_form.html', {
        'form': form,
        'title': 'Record New Payment'
    })

@login_required
@permission_required('finance.change_payment')
def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f'Payment updated successfully. Receipt: {payment.receipt_number}')
            return redirect('finance:payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'finance/payment_form.html', {'form': form, 'payment': payment})

@login_required
@permission_required('finance.delete_payment')
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        receipt_number = payment.receipt_number
        payment.delete()
        messages.success(request, f'Payment with receipt number {receipt_number} has been deleted.')
        return redirect('finance:payment_list')
    return render(request, 'finance/payment_confirm_delete.html', {'payment': payment})

@login_required
@permission_required('finance.view_scholarship')
def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'finance/scholarship_list.html', {'scholarships': scholarships})

@login_required
@permission_required('finance.add_scholarship')
def scholarship_create(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scholarship created successfully.')
            return redirect('finance:scholarship_list')
    else:
        form = ScholarshipForm()
    return render(request, 'finance/scholarship_form.html', {'form': form})

@login_required
def student_finance_summary(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student)
    scholarships = Scholarship.objects.filter(student=student)
    
    total_fees = Fee.objects.filter(semester=student.studentacademicinfo_set.first().current_semester).aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_scholarships = scholarships.filter(is_active=True).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_fees - total_paid - total_scholarships
    
    context = {
        'student': student,
        'payments': payments,
        'scholarships': scholarships,
        'total_fees': total_fees,
        'total_paid': total_paid,
        'total_scholarships': total_scholarships,
        'balance': balance,
    }
    return render(request, 'finance/student_finance_summary.html', context)

@login_required
@permission_required('finance.view_payment')
def payment_receipt(request, pk):
    payment = get_object_or_404(Payment.objects.select_related(
        'student',
        'fee'
    ), pk=pk)
    
    # Get academic info using the new related_name
    academic_info = payment.student.academic_info.first()
    
    context = {
        'payment': payment,
        'academic_info': academic_info,
    }
    return render(request, 'finance/payment_receipt.html', context)
