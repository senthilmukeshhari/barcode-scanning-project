from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    section_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ]
    bloodgroup_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    ]

    rollno = models.IntegerField(unique=True, primary_key=True)    
    name = models.CharField(max_length=100)
    email= models.EmailField(null=True, blank=True)
    phoneno = models.BigIntegerField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    section = models.CharField(choices=section_choices, max_length=10)
    dob = models.DateField()
    bloodgroup = models.CharField(max_length=10, choices=bloodgroup_choices)
    gender = models.CharField(choices=gender_choices, max_length=10)
    address = models.TextField()
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EntryExit(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return self.barcode