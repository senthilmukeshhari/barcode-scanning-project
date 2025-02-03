from django.contrib import admin
from .models import Department, Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('rollno', 'name', 'department', 'section', 'dob', 'is_active' )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Student, StudentAdmin)