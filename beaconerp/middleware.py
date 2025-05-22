from django.shortcuts import redirect
from django.urls import resolve
from django.contrib import messages

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_url = resolve(request.path_info).url_name
            app_name = resolve(request.path_info).app_name
            
            # Allow access to common pages
            if current_url in ['login', 'logout', 'password_reset', 'password_reset_done', 
                             'password_reset_confirm', 'password_reset_complete', 'dashboard']:
                return self.get_response(request)
                
            # Admin users have access to everything
            if request.user.is_superuser:
                return self.get_response(request)
                
            # Staff permissions
            if request.user.is_staff:
                allowed_apps = ['students', 'courses', 'attendance', 'instructors']
                if app_name in allowed_apps:
                    return self.get_response(request)
                    
            # Student permissions (implement based on your user model)
            if hasattr(request.user, 'student'):
                allowed_urls = ['student_profile', 'course_list', 'attendance_view']
                if current_url in allowed_urls:
                    return self.get_response(request)
                    
            # If no permission matches, redirect to dashboard with message
            messages.warning(request, "You don't have permission to access that page.")
            return redirect('home:dashboard')
            
        return self.get_response(request)
