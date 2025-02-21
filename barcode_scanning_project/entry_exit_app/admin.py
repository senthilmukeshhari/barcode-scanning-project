from django.contrib import admin
from .models import Department, Student, EntryExit

class StudentAdmin(admin.ModelAdmin):
    list_display = ('rollno', 'name', 'department', 'section', 'dob', 'is_active' )

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')

class EntryExitAdmin(admin.ModelAdmin):
    list_display = ('student', 'entry_time', 'exit_time')

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(EntryExit, EntryExitAdmin)