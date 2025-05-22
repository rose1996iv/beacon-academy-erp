# Beacon Academy ERP System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

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

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd erp
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Unix/macOS
    .\venv\Scripts\Activate   # Windows
    ```

3. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure the environment:
   - Copy `.env.example` to `.env` (if provided)
   - Update the environment variables as needed

5. Initialize the database:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser (admin account):

    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`

## Default Login Credentials

After setting up the superuser, you can use those credentials to login at `http://127.0.0.1:8000/login/`

## Project Structure

```text
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

## Project Screenshots

![Dashboard](docs/images/dashboard.png)

### Dashboard Overview

Dashboard view showing key metrics

## API Documentation

The API documentation is available at `/api/docs/` when running the server. Key endpoints include:

- `/api/students/` - Student management
- `/api/courses/` - Course management
- `/api/attendance/` - Attendance tracking
- `/api/finance/` - Financial operations

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Create a new Pull Request

## Development Environment

### Testing

We use Django's built-in testing framework along with pytest. To run tests:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test students
python manage.py test courses

# Run with coverage report
coverage run manage.py test
coverage report
```

### Code Style

We follow PEP 8 guidelines for Python code. Before committing, please run:

```bash
black .
flake8
```

## Deployment

The application can be deployed using Docker or traditional hosting. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Contact Information

For support or queries:

- Email: [beaconacademy@gmail.com](mailto:beaconacademy@gmail.com)

## License

© 2025 Beacon Academy. All rights reserved.
