from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student
from courses.models import Course
from instructors.models import Instructor
from attendance.models import Attendance
from finance.models import Payment
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates example test data for the Beacon Academy ERP system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Create test users
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@beaconacademy.edu',
            password='admin123'
        )

        # Create test instructors
        instructors = []
        instructor_data = [
            {'name': 'Professor Port', 'subject': 'Grimm Studies'},
            {'name': 'Glynda Goodwitch', 'subject': 'Combat'},
            {'name': 'Doctor Oobleck', 'subject': 'History'},
        ]

        for data in instructor_data:
            instructor = Instructor.objects.create(
                user=User.objects.create_user(
                    username=data['name'].lower().replace(' ', ''),
                    email=f"{data['name'].lower().replace(' ', '')}@beaconacademy.edu",
                    password='instructor123'
                ),
                name=data['name'],
                subject=data['subject']
            )
            instructors.append(instructor)

        # Create test courses
        courses = []
        course_data = [
            {'name': 'Grimm Studies 101', 'instructor': instructors[0]},
            {'name': 'Combat Training', 'instructor': instructors[1]},
            {'name': 'Remnant History', 'instructor': instructors[2]},
        ]

        for data in course_data:
            course = Course.objects.create(
                name=data['name'],
                instructor=data['instructor'],
                credits=4,
                description=f"Introduction to {data['name']}"
            )
            courses.append(course)

        # Create test students
        students = []
        student_data = [
            {'name': 'Ruby Rose', 'year': 1},
            {'name': 'Weiss Schnee', 'year': 1},
            {'name': 'Blake Belladonna', 'year': 1},
            {'name': 'Yang Xiao Long', 'year': 1},
        ]

        for data in student_data:
            student = Student.objects.create(
                user=User.objects.create_user(
                    username=data['name'].lower().replace(' ', ''),
                    email=f"{data['name'].lower().replace(' ', '')}@beaconacademy.edu",
                    password='student123'
                ),
                name=data['name'],
                year=data['year']
            )
            students.append(student)
            # Enroll students in courses
            for course in courses:
                student.courses.add(course)

        # Create attendance records
        for _ in range(30):  # Last 30 days
            date = datetime.now() - timedelta(days=_)
            for student in students:
                for course in courses:
                    if random.choice([True, True, False]):  # 2/3 chance of attendance
                        Attendance.objects.create(
                            student=student,
                            course=course,
                            date=date,
                            status='present'
                        )

        # Create payment records
        payment_types = ['tuition', 'books', 'housing']
        for student in students:
            for _ in range(3):
                Payment.objects.create(
                    student=student,
                    amount=random.randint(500, 2000),
                    payment_type=random.choice(payment_types),
                    date=datetime.now() - timedelta(days=random.randint(0, 90))
                )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
