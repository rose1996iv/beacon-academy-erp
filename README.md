# Beacon Academy ERP System

A comprehensive Educational Resource Planning (ERP) system for Beacon Academy, built with Django.

## Features

- Student Management
- Course Management
- Instructor Management
- Attendance Tracking
- Finance Management (Fees, Payments, Scholarships)
- User Authentication & Authorization
- Dashboard with Analytics

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

## Installation & Setup

1. Clone the repository
```powershell
git clone <repository-url>
cd erp
```

2. Create and activate a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install required packages
```powershell
pip install -r requirements.txt
```

4. Configure the environment
- Copy `.env.example` to `.env` (if provided)
- Update the environment variables as needed

5. Initialize the database
```powershell
python manage.py migrate
```

6. Create a superuser (admin account)
```powershell
python manage.py createsuperuser
```

7. Run the development server
```powershell
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Default Login Credentials

After setting up the superuser, you can use those credentials to login at:
`http://127.0.0.1:8000/login/`

## Project Structure

```
erp/
├── attendance/      # Attendance management
├── courses/        # Course management
├── finance/        # Financial management
├── instructors/    # Instructor management
├── students/       # Student management
├── users/          # User management
├── templates/      # HTML templates
└── static/         # Static files (CSS, JS, etc.)
```

## Key URLs

- Admin Interface: `/admin/`
- Dashboard: `/`
- Students List: `/students/`
- Courses List: `/courses/`
- Instructors List: `/instructors/`
- Attendance: `/attendance/`
- Finance: `/finance/`

## Development Notes

### Database Migrations

When making model changes:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Creating New Apps

```powershell
python manage.py startapp new_app_name
```

### Running Tests

```powershell
python manage.py test
```

## Contact Information

For support or queries:
- Email: beaconacademy@gmail.com

## License

© 2025 Beacon Academy. All rights reserved.
