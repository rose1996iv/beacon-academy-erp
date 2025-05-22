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
    today = timezone.now().date()
    
    try:
        # Calculate statistics
        context['total_students'] = Student.objects.filter(is_active=True).count()
        context['active_courses'] = Course.objects.filter(is_active=True).count()
        
        # Calculate today's attendance percentage
        today_attendance = AttendanceRecord.objects.filter(date=today)
        if today_attendance.exists():
            present_count = today_attendance.filter(status='P').count()
            total_count = today_attendance.count()
            context['attendance_percentage'] = round((present_count / total_count) * 100)
        else:
            context['attendance_percentage'] = None
        
        # Calculate fees statistics
        total_fees = Fee.objects.filter(is_active=True).aggregate(
            total=Sum('amount')
        )['total'] or 0
        total_paid = Payment.objects.filter(
            payment_date__lte=today
        ).aggregate(
            paid=Sum('amount_paid')
        )['paid'] or 0
        
        context['total_fees'] = total_fees
        context['total_paid'] = total_paid
        context['pending_fees'] = total_fees - total_paid
        
        # Get recent activities
        recent_activities = []
        
        # Recent attendance records
        recent_attendance = AttendanceRecord.objects.select_related(
            'student', 'course'
        ).order_by('-date', '-time_marked')[:5]
        
        for record in recent_attendance:
            recent_activities.append({
                'title': 'Attendance Marked',
                'description': f"{record.student.full_name} in {record.course.name}",
                'timestamp': record.time_marked,
                'type': 'attendance',
                'badge_type': 'info'
            })
        
        # Recent payments
        recent_payments = Payment.objects.select_related(
            'student', 'fee'
        ).order_by('-payment_date')[:5]
        
        for payment in recent_payments:
            recent_activities.append({
                'title': 'Payment Received',
                'description': f"{payment.student.full_name} paid {payment.amount_paid} for {payment.fee.name}",
                'timestamp': payment.payment_date,
                'type': 'payment',
                'badge_type': 'success'
            })
        
        # Sort activities by timestamp
        recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        context['recent_activities'] = recent_activities[:10]
        
        # Get upcoming events
        upcoming_events = []
        
        # Upcoming fee due dates
        upcoming_fees = Fee.objects.filter(
            due_date__gte=today
        ).order_by('due_date')[:5]
        
        for fee in upcoming_fees:
            upcoming_events.append({
                'title': f"{fee.name} payment due",
                'date': fee.due_date,
                'type': 'fee_due',
                'description': f"Amount: {fee.amount}"
            })
        
        context['upcoming_events'] = upcoming_events
        
        # Add attendance trends
        attendance_trends = AttendanceRecord.objects.filter(
            date__gte=today - timezone.timedelta(days=7)
        ).annotate(
            day=TruncDay('date')
        ).values('day').annotate(            total=Count('id'),
            present=Count('id', filter=Q(status='P'))
        ).order_by('day')
        
        context['attendance_trends'] = [{
            'date': record['day'],
            'percentage': round((record['present'] / record['total']) * 100)
            if record['total'] > 0 else 0
        } for record in attendance_trends]

    except Exception as e:
        messages.error(request, f"Error loading dashboard data: {str(e)}")
        context['error'] = str(e)
    
    return render(request, 'home/dashboard.html', context)
