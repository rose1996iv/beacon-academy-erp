from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Fee management
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/create/', views.fee_create, name='fee_create'),
    path('fees/<int:pk>/edit/', views.fee_edit, name='fee_edit'),
    path('fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),
    
    # Payment management
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('payments/<int:pk>/receipt/', views.payment_receipt, name='payment_receipt'),
    
    # Scholarship management
    path('scholarships/', views.scholarship_list, name='scholarship_list'),
    path('scholarships/create/', views.scholarship_create, name='scholarship_create'),
    
    # Student finance summary
    path('student/<int:student_id>/', views.student_finance_summary, name='student_finance_summary'),
]
