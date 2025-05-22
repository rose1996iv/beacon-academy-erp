from django.contrib import admin
from .models import Fee, Payment, Scholarship

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'semester', 'due_date', 'is_active')
    list_filter = ('semester', 'is_active', 'due_date')
    search_fields = ('name', 'description')
    date_hierarchy = 'due_date'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee', 'amount_paid', 'payment_date', 'payment_method', 'receipt_number')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('student__full_name', 'receipt_number', 'transaction_id')
    date_hierarchy = 'payment_date'
    raw_id_fields = ('student', 'fee')

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'amount', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'student__full_name', 'description')
    date_hierarchy = 'start_date'
    raw_id_fields = ('student',)
