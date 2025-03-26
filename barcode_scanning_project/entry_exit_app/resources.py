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
    class Meta:
        model = EntryExit
        fields = ('student', 'student__name', 'student__department__name', 'student__section', 'entry_time', 'exit_time')