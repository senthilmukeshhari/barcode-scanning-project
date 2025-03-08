from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields
from .models import Student, EntryExit, Department

class StudentResource(resources.ModelResource):
    department = fields.Field(
        column_name= 'department',
        attribute= 'department',
        widget= ForeignKeyWidget(Department, 'name')
    )

    class Meta:
        model = Student
        fields = ('rollno', 'name', 'department', 'section', 'email', 'phoneno', 'dob', 'bloodgroup', 'gender', 'address', 'is_active', 'created_at', 'updated_at')

class EntryExitResource(resources.ModelResource):
    student = fields.Field(
        column_name='student',
        attribute= 'student',
        widget= ForeignKeyWidget(Student, 'name')
    )

    class Meta:
        model = EntryExit
        fields = ('student', 'entry_time', 'exit_time')