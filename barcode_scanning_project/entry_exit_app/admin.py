from django.contrib import admin
from .models import Department, Student, EntryExit
from django.contrib.auth.models import Group,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin,ExportActionModelAdmin
from .resources import StudentResource, EntryExitResource

from unfold.admin import ModelAdmin as UnfoldModalAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.contrib.import_export.forms import ImportForm, ExportForm, SelectableFieldsExportForm
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from unfold.contrib.filters.admin import ChoicesDropdownFilter, MultipleChoicesDropdownFilter

admin.site.unregister(Group)
admin.site.unregister(User)

@admin.action(description="Activate selected Students")
def activate_students(self, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Students")
def deactivate_students(self, request, queryset):
    queryset.update(is_active=False)

@admin.action(description="Activate selected Departments")
def activate_departments(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.action(description="Deactivate selected Departments")
def deactivate_departments(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModalAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Student)
class StudentAdmin(UnfoldModalAdmin, ExportActionModelAdmin):
    list_display = ('rollno', 'name', 'department', 'section', 'dob', 'admission_year', 'is_active')
    search_fields = ('rollno__iexact', 'name')
    search_help_text = 'Search by student rollno or name'
    list_filter = ('department', 'section', 'admission_year', 'is_active')
    list_per_page = 20
    actions = [activate_students, deactivate_students]
    change_form_show_cancel_button = True 
    list_filter_submit = True
    export_form_class = SelectableFieldsExportForm
    resource_class = StudentResource

@admin.register(Department)
class DepartmentAdmin(UnfoldModalAdmin, ExportActionModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    search_help_text = 'Search by department name'
    list_filter = ('is_active',)
    actions = [activate_departments, deactivate_departments]
    list_filter_submit = True
    change_form_show_cancel_button = True 
    export_form_class = SelectableFieldsExportForm


from django.db.models import F, ExpressionWrapper, fields, Sum
@admin.register(EntryExit)
class EntryExitAdmin(UnfoldModalAdmin, ExportActionModelAdmin):
    list_display = ('rollno', 'student', 'department', 'section', 'lab', 'entry_time', 'exit_time', 'time_spend_in_lab')
    search_fields = ('student__rollno__iexact', 'student__name')
    search_help_text = 'Search by student rollno or name'
    change_form_show_cancel_button = True
    list_filter_submit = True
    list_filter = (
        ("entry_time", RangeDateFilter),  # Date filter
        'lab',
        'student__department',
        ('student__section', MultipleChoicesDropdownFilter)
    )
    resource_class = EntryExitResource
    export_form_class = SelectableFieldsExportForm

    def section(self, obj):
        return obj.student.section
    
    def department(self, obj):
        return obj.student.department.name
    
    def rollno(self, obj):
        return obj.student.rollno
    