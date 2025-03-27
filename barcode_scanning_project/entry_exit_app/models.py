from django.db import models
import os

def getFilename(rollno, filename):
    extension = filename.split('.')[-1]
    new_filename = f"{rollno}.{extension}"
    return os.path.join('students/', new_filename)

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
    admission_year = models.PositiveSmallIntegerField()
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to=getFilename, null=True, blank=True, default='students/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rollno']

    def __str__(self):
        return self.name

class EntryExit(models.Model):
    lab_choices = [
        ('Lab-1' , 'Lab-1'),
        ('Lab-2' , 'Lab-2'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    lab = models.CharField(choices=lab_choices, max_length=10)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return str(self.student)
    
    @property
    def time_spend_in_lab(self):
        time_spend = "Not Exit"
        if self.exit_time:
            duration = self.exit_time - self.entry_time
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            parts = []
            if hours > 0:
                parts.append(f"{hours} hours")
            if minutes > 0:
                parts.append(f"{minutes} minutes")
            if seconds > 0:
                parts.append(f"{seconds} seconds")
            time_spend = ' '.join(parts)
        return time_spend