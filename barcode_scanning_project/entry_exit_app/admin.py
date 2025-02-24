from django.contrib import admin
from .models import Department, Student, EntryExit
from unfold.admin import ModelAdmin as UnfoldModalAdmin
from unfold.decorators import action
from unfold.contrib.filters.admin import RangeDateFilter, RangeDateTimeFilter
from import_export.admin import ImportExportModelAdmin


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

@admin.register(Student)
class StudentAdmin(UnfoldModalAdmin, ImportExportModelAdmin):
    list_display = ('rollno', 'name', 'department', 'section', 'dob', 'is_active')
    search_fields = ('rollno', 'name')
    list_filter = ('department', 'is_active')
    list_per_page = 20
    actions = [activate_students, deactivate_students]
    change_form_show_cancel_button = True 
    list_filter_submit = True

@admin.register(Department)
class DepartmentAdmin(UnfoldModalAdmin, ImportExportModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)
    actions = [activate_departments, deactivate_departments]
    list_filter_submit = True
    change_form_show_cancel_button = True 

@admin.register(EntryExit)
class EntryExitAdmin(UnfoldModalAdmin, ImportExportModelAdmin):
    list_display = ('student', 'entry_time', 'exit_time')
    search_fields = ('student__rollno', 'student__name')
    change_form_show_cancel_button = True 
    list_filter_submit = True
    list_filter = (
        'student__department',
        ("entry_time", RangeDateFilter),  # Date filter
        # ("field_F", RangeDateTimeFilter),  # Datetime filter
    )