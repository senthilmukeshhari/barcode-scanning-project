from django.db import models
from entry_exit_app.models import Department, Student
from faker import Faker
import random
import datetime

fake = Faker()

def generate_departments():
    departments = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL']
    for department in departments:
        deptObj = Department.objects.create(name=department)
        deptObj.save()

def generate_students(n):
    for i in range(n):
        rollno = i
        name = fake.name()
        email = fake.email()
        phoneno = fake.random_number()
        department = Department.objects.get(id=random.randint(1, 5))
        section = random.choice(['A', 'B', 'C', 'D'])
        dob = fake.date_of_birth()
        bloodgroup = random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
        address = fake.address()
        is_active = random.choice([True, False])
        student = Student.objects.create(rollno=rollno, name=name, email=email, phoneno=phoneno, department=department, section=section, dob=dob, bloodgroup=bloodgroup, address=address, is_active=is_active)
        student.save()

