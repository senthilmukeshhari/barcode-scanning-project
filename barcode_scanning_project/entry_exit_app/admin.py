from django.contrib import admin
from .models import Department, Student, EntryExit, Lab
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
from django.utils.timezone import now
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

    
    change_list_template = "admin/entry_exit_app/entryexit/change_list.html"

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_queryset(request)
        extra_context = extra_context or {}

        from datetime import timedelta
        from django.db.models import F, ExpressionWrapper, fields, Count
        from datetime import datetime
        from django.db.models.functions import TruncDate

        # **🔹 1. Only Show "Total Lab Hours per Student" Chart When Searching**
        student_labels = []
        student_data = []
        daily_labels = []
        daily_data = []
        
        if "q" in request.GET and request.GET["q"]:  # Check if search is performed
            if request.GET["q"].isdigit():
                rollno = request.GET["q"]
                queryset = queryset.filter(student__rollno = rollno)
                if queryset:
                    from entry_exit_app import views
                    student_labels , student_data = views.total_lab_hours_per_student_current_month(queryset)

        if request.GET.get("lab__id__exact"):  # Check if lab filter is applied
            # **🔹 2. Daily Lab Usage Trend**
            # Get data for the last 7 days
            lab_id = request.GET.get("lab__id__exact")
            last_week = now() - timedelta(days=7)
            print(last_week)
             # Filter for a specific lab and group by date
            daily_usage = (
                EntryExit.objects.filter(entry_time__gte=last_week, lab__id=lab_id)
                .annotate(date=TruncDate("entry_time"))
                .values("date")
                .annotate(total_visits=Count("id"))
                .order_by("date")
            ) 

            # Format labels and data
            daily_labels = [entry["date"].strftime("%Y-%m-%d") for entry in daily_usage]
            daily_data = [entry["total_visits"] for entry in daily_usage]

        # **🔹 Pass Data to Template**
        extra_context.update({
            "student_labels": student_labels if student_labels else None,
            "student_data": student_data if student_data else None,
            "daily_labels": daily_labels if daily_labels else None, 
            "daily_data": daily_data if daily_data else None,
        })
        print(extra_context)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Lab)
class LabAdmin(UnfoldModalAdmin):
    list_display = ('name', 'department', 'in_charge')
    search_fields = ('name', 'in_change')
    search_help_text = "Search by lab name or in charge name"
    list_filter = ('department__name',)
    change_form_show_cancel_button = True
    list_filter_submit = True

    def department(self, obj):
        return obj.student.department.name
