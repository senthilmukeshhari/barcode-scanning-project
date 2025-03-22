from entry_exit_app.models import Department, Student
from faker import Faker
import random

fake = Faker()

def generate_departments():
    departments = ['BCA', 'BCS', 'B.sc(IT)', 'B.Com', 'B.A Tamil']
    for department in departments:
        deptObj = Department.objects.filter(name=department)
        if not deptObj.exists():
            deptObj = Department.objects.create(name=department)
            deptObj.save()
        else:
            print(f'Alreay Exisit Department of {department}...')

def generate_students(n):
    for i in range(1,n+1):
        stu_obi = Student.objects.filter(rollno=i)
        if not stu_obi.exists():
            rollno = i
            name = fake.name()
            email = fake.email()
            phoneno = fake.random_number()
            department = Department.objects.get(id=random.randint(1, 5))
            section = random.choice(['A', 'B', 'C', 'D'])
            dob = fake.date_of_birth()
            bloodgroup = random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
            gender = random.choice(['Male', 'Female', 'Other'])
            address = fake.address()
            is_active = True
            student = Student.objects.create(rollno=rollno, name=name, email=email, phoneno=phoneno, department=department, section=section, dob=dob, bloodgroup=bloodgroup, gender=gender, address=address, is_active=is_active)
            student.save()
        else:
            print(f'Alreay Exisit Student of {i}...')