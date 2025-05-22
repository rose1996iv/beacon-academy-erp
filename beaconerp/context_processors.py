def user_role(request):
    """Add user role information to the template context."""
    context = {
        'is_admin': request.user.is_superuser if request.user.is_authenticated else False,
        'is_staff': request.user.is_staff if request.user.is_authenticated else False,
        'is_student': hasattr(request.user, 'student') if request.user.is_authenticated else False,
    }
    return context
