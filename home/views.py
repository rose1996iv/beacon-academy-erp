from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from students.models import Student
from courses.models import Course
from attendance.models import AttendanceRecord
from finance.models import Fee, Payment
from django.contrib import messages

@login_required
def dashboard(request):
    context = {}
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    try:
        # Calculate statistics
        context['total_students'] = Student.objects.filter(is_active=True).count()
        context['active_courses'] = Course.objects.filter(is_active=True).count()
        
        # Calculate today's attendance percentage
        today_attendance = AttendanceRecord.objects.filter(date=now.date())
        if today_attendance.exists():
            present_count = today_attendance.filter(status='P').count()
            total_count = today_attendance.count()
            context['attendance_percentage'] = round((present_count / total_count) * 100)
        else:
            context['attendance_percentage'] = None
            
        # Calculate fees statistics
        current_fees = Fee.objects.filter(is_active=True, due_date__gte=now.date())
        context['pending_fees'] = current_fees.aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate payments for today
        today_payments = Payment.objects.filter(
            payment_date=now.date()
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        context['today_payments'] = today_payments
        
        # Attendance trend for the last 7 days
        attendance_trend = AttendanceRecord.objects.filter(
            date__gte=now.date() - timezone.timedelta(days=7),
            date__lte=now.date()
        ).values('date').annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status='P'))
        ).order_by('date')
        
        context['attendance_trend'] = [{
            'date': record['date'].strftime('%Y-%m-%d'),
            'percentage': round((record['present'] / record['total']) * 100) if record['total'] > 0 else 0
        } for record in attendance_trend]
        
        # Payment trend for the last 7 days
        payment_trend = Payment.objects.filter(
            payment_date__gte=now.date() - timezone.timedelta(days=7),
            payment_date__lte=now.date()
        ).values('payment_date').annotate(
            paid=Sum('amount_paid')
        ).order_by('payment_date')
        
        context['payment_trend'] = [{
            'date': record['payment_date'].strftime('%Y-%m-%d'),
            'amount': float(record['paid']) if record['paid'] else 0
        } for record in payment_trend]

    except Exception as e:
        messages.error(request, f'Error loading dashboard data: {str(e)}')
        context['error'] = True
    
    return render(request, 'home/dashboard.html', context)
