from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='list'),
    path('mark/', views.mark_attendance, name='mark'),
    path('report/', views.attendance_report, name='report'),
    path('course/<int:course_id>/', views.course_attendance, name='course'),
    path('student/<int:student_id>/', views.student_attendance, name='student'),
    path('edit/<int:pk>/', views.attendance_edit, name='edit'),
    path('delete/<int:pk>/', views.attendance_delete, name='delete'),
    path('get_enrolled_students/<int:course_id>/', views.get_enrolled_students, name='get_enrolled_students'),
]