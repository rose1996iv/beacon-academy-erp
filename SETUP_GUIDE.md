# Beacon ERP System - Setup and Run Guide

## Project Setup Instructions

1. Virtual Environment Setup:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate
```

2. Install Required Packages:
```powershell
pip install django pillow
```

3. Database Setup:
```powershell
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

4. Create Superuser:
```powershell
python manage.py createsuperuser
```
Enter the following details when prompted:
- Username: admin
- Email: admin@example.com
- Password: (your chosen password)

5. Collect Static Files:
```powershell
python manage.py collectstatic --noinput
```

6. Run Development Server:
```powershell
python manage.py runserver
```

## Accessing the System

1. Main URLs:
- Admin Panel: http://127.0.0.1:8000/admin/
- Login Page: http://127.0.0.1:8000/login/
- Dashboard: http://127.0.0.1:8000/

2. User Types:
- Admin: Full access to all features
- Staff: Access to manage students, courses, attendance
- Students: Limited access to view their own data

## Common Issues and Solutions

1. Static Files Not Loading:
- Ensure STATIC_ROOT and STATIC_URL are properly set in settings.py
- Run collectstatic command

2. Database Errors:
- Delete db.sqlite3 file
- Delete all migration files (except __init__.py)
- Run makemigrations and migrate commands

3. Permission Issues:
- Login as admin
- Grant appropriate permissions through admin panel

4. Template Not Found:
- Check TEMPLATES setting in settings.py
- Verify template files exist in correct directories

## Development Workflow

1. Make changes to models:
```powershell
python manage.py makemigrations
python manage.py migrate
```

2. Test changes:
```powershell
python manage.py test
```

3. Run server with debug toolbar:
```powershell
pip install django-debug-toolbar
```
Add 'debug_toolbar' to INSTALLED_APPS

## Deployment Checklist

1. Update settings.py:
- Set DEBUG = False
- Update ALLOWED_HOSTS
- Configure production database
- Set up proper email backend

2. Security settings:
- Generate new SECRET_KEY
- Enable HTTPS
- Configure proper session settings

3. Static/Media files:
- Set up proper static file serving
- Configure media file storage

## Backup and Maintenance

1. Database backup:
```powershell
python manage.py dumpdata > backup.json
```

2. Restore database:
```powershell
python manage.py loaddata backup.json
```

3. Regular maintenance:
- Update Django and other packages
- Monitor error logs
- Backup database regularly
