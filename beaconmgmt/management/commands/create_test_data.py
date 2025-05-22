from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from students.models import Student, StudentAcademicInfo
from courses.models import Course, CourseSchedule
from instructors.models import Instructor, CourseInstructor
from attendance.models import AttendanceRecord
from finance.models import Fee, Payment
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates example test data for the Beacon Academy ERP system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')
        
        try:
            with transaction.atomic():
                # Clean up existing test data
                self.stdout.write('Cleaning up existing test data...')
                Payment.objects.all().delete()
                Fee.objects.all().delete()
                AttendanceRecord.objects.all().delete()
                StudentAcademicInfo.objects.all().delete()
                Student.objects.all().delete()
                CourseSchedule.objects.all().delete()
                CourseInstructor.objects.all().delete()
                Course.objects.all().delete()
                Instructor.objects.all().delete()
                User.objects.filter(is_superuser=False).delete()
                User.objects.filter(username='admin').delete()

                # Create test users
                admin = User.objects.create_superuser(
                    username='admin',
                    email='admin@beaconacademy.edu',
                    password='admin123'
                )

                # Create test instructors
                instructors = []
                instructor_data = [
                    {
                        'first_name': 'Peter', 'last_name': 'Port',
                        'specialization': 'Grimm Studies',
                        'qualifications': 'PhD in Grimm Studies, Master Hunter',
                        'experience': 15
                    },
                    {
                        'first_name': 'Glynda', 'last_name': 'Goodwitch',
                        'specialization': 'Combat',
                        'qualifications': 'Master of Combat Arts, Advanced Dust Manipulation',
                        'experience': 12
                    },
                    {
                        'first_name': 'Bartholomew', 'last_name': 'Oobleck',
                        'specialization': 'History',
                        'qualifications': 'PhD in Remnant History, Expert in Archaeological Studies',
                        'experience': 10
                    },
                ]

                for data in instructor_data:
                    user = User.objects.create_user(
                        username=f"{data['first_name'].lower()}{data['last_name'].lower()}",
                        email=f"{data['first_name'].lower()}.{data['last_name'].lower()}@beaconacademy.edu",
                        password='instructor123',
                        first_name=data['first_name'],
                        last_name=data['last_name']
                    )
                    instructor = Instructor.objects.create(
                        user=user,
                        phone='+1234567890',
                        address='Beacon Academy, Vale',
                        specialization=data['specialization'],
                        qualifications=data['qualifications'],
                        teaching_experience=data['experience'],
                        bio=f"Experienced instructor in {data['specialization']}",
                        emergency_contact_name='Emergency Contact',
                        emergency_contact_phone='+0987654321'
                    )
                    instructors.append(instructor)

                # Create test courses
                courses = []
                course_data = [
                    {
                        'code': 'GRM101',
                        'name': 'Grimm Studies 101',
                        'description': 'Introduction to the study of Grimm, their behaviors, and combat tactics',
                        'department': 'Combat Studies'
                    },
                    {
                        'code': 'CBT201',
                        'name': 'Combat Training',
                        'description': 'Advanced combat techniques and dust manipulation',
                        'department': 'Combat Studies'
                    },
                    {
                        'code': 'HST101',
                        'name': 'Remnant History',
                        'description': 'Survey of the history of Remnant and its four kingdoms',
                        'department': 'General Studies'
                    },
                ]

                for data in course_data:
                    course = Course.objects.create(
                        code=data['code'],
                        name=data['name'],
                        description=data['description'],
                        credits=4,
                        semester=1,
                        department=data['department'],
                        is_active=True
                    )
                    courses.append(course)

                # Create course schedules
                days = ['MON', 'WED', 'FRI']
                times = [
                    ('09:00:00', '10:30:00'),
                    ('11:00:00', '12:30:00'),
                    ('14:00:00', '15:30:00')
                ]

                for course, (day, time) in zip(courses, zip(days, times)):
                    CourseSchedule.objects.create(
                        course=course,
                        day=day,
                        start_time=time[0],
                        end_time=time[1],
                        room=f'Room {random.randint(101, 110)}'
                    )

                # Assign instructors to courses
                for course, instructor in zip(courses, instructors):
                    CourseInstructor.objects.create(
                        instructor=instructor,
                        course=course,
                        is_primary=True,
                        notes=f'Primary instructor for {course.name}'
                    )

                # Create test students
                students = []
                student_data = [
                    {
                        'full_name': 'Ruby Rose',
                        'dob': '2008-10-31',
                        'gender': 'F',
                        'student_id': '2025001'
                    },
                    {
                        'full_name': 'Weiss Schnee',
                        'dob': '2008-05-15',
                        'gender': 'F',
                        'student_id': '2025002'
                    },
                    {
                        'full_name': 'Blake Belladonna',
                        'dob': '2008-01-19',
                        'gender': 'F',
                        'student_id': '2025003'
                    },
                    {
                        'full_name': 'Yang Xiao Long',
                        'dob': '2007-07-28',
                        'gender': 'F',
                        'student_id': '2025004'
                    },
                ]

                for data in student_data:
                    email = f"{data['full_name'].lower().replace(' ', '.')}@beaconacademy.edu"
                    student = Student.objects.create(
                        student_id=data['student_id'],
                        full_name=data['full_name'],
                        date_of_birth=data['dob'],
                        gender=data['gender'],
                        address='Beacon Academy, Vale',
                        phone='+1234567890',
                        email=email
                    )
                    students.append(student)

                    # Create academic info
                    StudentAcademicInfo.objects.create(
                        student=student,
                        current_semester=1,
                        batch='2025',
                        department='Huntsman Training',
                        cgpa=None  # First-year students don't have CGPA yet
                    )

                # Create attendance records
                for _ in range(30):  # Last 30 days
                    date = datetime.now() - timedelta(days=_)
                    for student in students:
                        for course in courses:
                            if random.choice([True, True, False]):  # 2/3 chance of attendance
                                # Get primary instructor for the course
                                course_instructor = CourseInstructor.objects.get(course=course, is_primary=True)
                                AttendanceRecord.objects.create(
                                    student=student,
                                    course=course,
                                    date=date,
                                    status='P',  # Present
                                    marked_by=course_instructor.instructor,
                                    notes='Regular class attendance'
                                )

                # Create fees
                fee_types = [
                    {'name': 'Tuition Fee', 'amount': 5000},
                    {'name': 'Books and Materials', 'amount': 800},
                    {'name': 'Housing Fee', 'amount': 3000}
                ]
                
                fees = []
                for fee_type in fee_types:
                    fee = Fee.objects.create(
                        name=fee_type['name'],
                        amount=fee_type['amount'],
                        semester=1,
                        description=f"Standard {fee_type['name'].lower()} for semester 1",
                        due_date=datetime.now() + timedelta(days=30),
                        is_active=True
                    )
                    fees.append(fee)

                # Create payment records
                payment_methods = ['CASH', 'CARD', 'TRANSFER', 'CHECK']
                for student in students:
                    for fee in fees:
                        # Random partial or full payment
                        amount_paid = round(fee.amount * random.uniform(0.5, 1.0), 2)
                        Payment.objects.create(
                            student=student,
                            fee=fee,
                            amount_paid=amount_paid,
                            payment_method=random.choice(payment_methods),
                            transaction_id=f"TXN-{random.randint(10000, 99999)}",
                            receipt_number=f"RN-{student.id}-{fee.id}-{random.randint(1000, 9999)}",
                            notes=f"Initial payment for {fee.name.lower()}"
                        )

                self.stdout.write(self.style.SUCCESS('Successfully created test data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating test data: {str(e)}'))
            raise
