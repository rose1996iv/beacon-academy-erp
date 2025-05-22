from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Fee management
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/create/', views.fee_create, name='fee_create'),
    
    # Payment management
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    
    # Scholarship management
    path('scholarships/', views.scholarship_list, name='scholarship_list'),
    path('scholarships/create/', views.scholarship_create, name='scholarship_create'),
    
    # Student finance summary
    path('student/<int:student_id>/', views.student_finance_summary, name='student_finance_summary'),
]
