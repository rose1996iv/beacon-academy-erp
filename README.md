# Beacon Academy ERP System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

A comprehensive Educational Resource Planning (ERP) system for Beacon Academy, built with Django.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Test Data](#test-data)
- [Branch Structure](#branch-structure)
- [Live Testing](#live-testing)
- [Documentation](#documentation)

## Features

The Beacon Academy ERP system includes:

- Student Management
- Course Management
- Instructor Management
- Attendance Tracking
- Finance Management (Fees, Payments, Scholarships)
- User Authentication & Authorization
- Dashboard with Analytics

## Prerequisites

Before you begin, ensure you have:

- Python 3.10 or higher
- Git
- A virtual environment tool

## Development Setup

Follow these steps to set up your development environment:

1. Clone the repository:

```bash
git clone https://github.com/rose1996iv/beacon-academy-erp.git
cd beacon-academy-erp
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## Test Data

To populate the system with test data for development:

```bash
python manage.py create_test_data
```

This creates:

- Admin user:
  - Username: `admin`
  - Password: `admin123`

- Test instructors:
  - Professor Port (`peterport/instructor123`)
  - Glynda Goodwitch (`glyndagoodwitch/instructor123`)
  - Doctor Oobleck (`bartholomewoobleck/instructor123`)

- Test students:
  - Ruby Rose (ID: 2025001)
  - Weiss Schnee (ID: 2025002)
  - Blake Belladonna (ID: 2025003)
  - Yang Xiao Long (ID: 2025004)

## Branch Structure

The repository uses a three-tier branch structure:

- `main` - Production-ready code
- `staging` - Pre-production testing
- `development` - Active development

## Live Testing

The system can be tested at different stages:

- Development: `http://localhost:8000`
- Staging: See deployment guide
- Production: See deployment guide

### Test Environment Access

Different user roles are available for testing:

1. Administrator:
   - URL: `http://localhost:8000/admin`
   - Username: `admin`
   - Password: `admin123`

2. Instructor Portal:
   - URL: `http://localhost:8000/instructors`
   - Example: Username: `peterport`, Password: `instructor123`

3. Student Portal:
   - URL: `http://localhost:8000/students`
   - Access via student IDs

## Documentation

- [Setup Guide](SETUP_GUIDE.md)
- [GitHub Guide](GITHUB_GUIDE.md)
- [Deployment Guide](DEPLOYMENT.md)

## Contact

For support or inquiries:
- Email: beaconacademy@gmail.com

## License

© 2025 Beacon Academy. All rights reserved.
