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
@permission_required('finance.view_payment')
def payment_list(request):
    payments = Payment.objects.all().order_by('-payment_date')
    return render(request, 'finance/payment_list.html', {'payments': payments})

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
    return render(request, 'finance/payment_form.html', {'form': form})

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
