from django.shortcuts import render, get_object_or_404
from entry_exit_app.models import EntryExit, Student, Department, Lab
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import datetime
import json

def get_status_and_users_in_lab(lab):
    today = now().date()
    students = EntryExit.objects.filter(lab=lab, entry_time__date=today, exit_time__isnull=True)
    students_in_lab = EntryExit.objects.filter(lab=lab, entry_time__date=today).count()
    lab_status =f'There are {students.count()} user(s) in the {lab.name}.' if students.count() > 0 else f'No one in the {lab.name} currently.'
    return students_in_lab, lab_status

def get_initial_notifications(lab):
    today = now().date()
    entries = EntryExit.objects.filter(lab=lab, entry_time__date=today).order_by('-entry_time')
    notifications = []
    for entry in entries:
        if entry.exit_time:
            notifications.append(f"Student {entry.student.rollno} exited the {entry.lab.name}.")
        notifications.append(f"Student {entry.student.rollno} entered the {entry.lab.name}.")
    return notifications

def context_data(lab_id):
    lab = Lab.objects.get(id=lab_id)
    students_in_lab, lab_status = get_status_and_users_in_lab(lab)
    notifications = get_initial_notifications(lab)
    context = {
        'students_in_lab' : students_in_lab,
        'lab_status': lab_status,
        'notifications': notifications
    }
    return context
    
def home(request):
    context = {
        'website_name' : 'College Lab Entry/Exit System'
    }
    if request.method == 'POST':
        if request.POST['lab']:
            lab_id = request.POST['lab']
            context = context_data(lab_id)
            context['selected_lab'] = lab_id
            print(context)
    context['labs'] = Lab.objects.all()
    return render(request, 'home.html', context=context)

def update_context_with_student_data(context, lab, entry_exit_log, status):
    context['student'] = entry_exit_log.student.rollno
    context['student_name'] = entry_exit_log.student.name
    context['department'] = entry_exit_log.student.department.name
    context['section'] = entry_exit_log.student.section
    context['profile_image'] = entry_exit_log.student.profile_image.url
    context['entry_time'] = entry_exit_log.entry_time.strftime('%Y-%m-%d %H:%M:%S') if status == 'enter' else None
    context['exit_time'] = entry_exit_log.exit_time.strftime('%Y-%m-%d %H:%M:%S') if status == 'exit' else None
    context['students_in_lab'], context['lab_status'] = get_status_and_users_in_lab(lab)
    context['notification'] = f"Student {entry_exit_log.student.rollno} {status}ed the {entry_exit_log.lab.name}."

def scan_barcode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            barcode = data['barcode']
            lab_id = data['lab']
            year = int(data['year'])
            current_year = datetime.now().year
            student = get_object_or_404(Student, rollno=barcode, is_active=True)

            if(student.admission_year != current_year - year):
                year = 'I' if (year == 1) else 'II' if (year == 2) else 'III'
                return JsonResponse({
                    'status': 'error',
                    'message': f'Only allow {year} year students.',
                }, status=400)
            
            context = context_data(lab_id)
            lab = Lab.objects.get(id=lab_id)
            open_log = EntryExit.objects.filter(student=student, lab = lab, exit_time__isnull=True).first()

            if open_log:
                open_log.exit_time = now()
                open_log.save()
                update_context_with_student_data(context, lab, open_log, 'exit')
                return JsonResponse({
                    'status': 'exit',
                    'message': 'Exit logged successfully.',
                    'data': context
                }, status=201)

            new_entry = EntryExit.objects.create(student=student, lab = lab, entry_time=now())
            update_context_with_student_data(context, lab, new_entry, 'enter')
            return JsonResponse({
                'status': 'entry',
                'message': 'Entry logged successfully.',
                'data': context
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        
        except Student.DoesNotExist:
            print('Does not : ')
            return JsonResponse({
                'status': 'error',
                'message': 'barcode'
            }, status=400)
        
        except Exception as e:
            print('error : ', e)
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid barcode'
            }, status=400)


from datetime import timedelta
from django.db.models import F, ExpressionWrapper, fields, Count
from datetime import datetime
from django.db.models.functions import TruncDate

def dashboard_callback(request, context):
    queryset = EntryExit.objects.all()
    # **🔹 1. Lab-wise Usage Report** # Aggregate lab usage data
     # Aggregate lab usage data grouped by department
    lab_usage = (
        EntryExit.objects.values("lab__name", "lab__department__name", "lab__in_charge")
        .annotate(total_entries=Count("id"))
        .order_by("lab__department__name", "-total_entries")  # Sort by department, then total entries
    )
    lab_labels = []
    lab_data = []

    for entry in lab_usage:
        lab_labels.append(entry["lab__name"] + " (" + entry["lab__department__name"] + ")")
        lab_data.append(entry["total_entries"])

    # **🔹 2. Student with Most Lab Visits (Leaderboard)**
    student_leaderboard = (
        EntryExit.objects.values("student__name", "student__rollno")
        .annotate(total_visits=Count("id"))
        .order_by("-total_visits")[:5]  # Get top 5 students
    )

    leaderboard = [
        [ index + 1, entry["student__name"], entry["student__rollno"], entry["total_visits"] ] for index, entry in enumerate(student_leaderboard)
    ]

    last_week = now() - timedelta(days=7)
    daily_usage = (
        queryset.filter(entry_time__gte=last_week)
        .annotate(date=TruncDate("entry_time"))
        .values("date")
        .annotate(total_visits=Count("id"))
        .order_by("date")
    )

    # Prepare Labels & Data
    daily_labels = [entry["date"].strftime("%Y-%m-%d") for entry in daily_usage]
    daily_data = [entry["total_visits"] for entry in daily_usage]

    context.update(
        {
            "lab_labels": lab_labels, "lab_data": lab_data,
            "table_data" : {
                "headers" : ["Rank", "Student Name", "Student Rollno", "Total Visits"],
                "rows": leaderboard,
            }
        }
    )

    return context

import datetime
import calendar
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Sum, F, ExpressionWrapper, DurationField
def total_lab_hours_per_student_current_month(queryset):
    # Determine the start (Monday) and end (Sunday) of the current week
    today = now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + datetime.timedelta(days=6)           # Sunday

    # Filter records for the current week and annotate each record with day and duration
    qs = queryset.filter(
        entry_time__date__gte=start_of_week,
        entry_time__date__lte=end_of_week
    ).annotate(
        day=TruncDate('entry_time'),
        duration=ExpressionWrapper(F('exit_time') - F('entry_time'), output_field=DurationField())
    )

    # Aggregate total duration per student per day
    aggregation = qs.values('student__name', 'day').annotate(
        total_duration=Sum('duration')
    ).order_by('student__name', 'day')

    # Build a dictionary: { student_name: { day_str: total_hours, ... }, ... }
    data = {}
    for entry in aggregation:
        student = entry['student__name']
        day_str = entry['day'].strftime('%Y-%m-%d')
        hours = entry['total_duration'].total_seconds() / 3600 if entry['total_duration'] else 0
        if hours < 0:
            hours = 0
        if student not in data:
            data[student] = {}
        data[student][day_str] = hours

    # Create a list of all days in the current week (as strings)
    days = []
    current_day = start_of_week
    while current_day <= end_of_week:
        days.append(current_day.strftime('%Y-%m-%d'))
        current_day += datetime.timedelta(days=1)

    # Prepare datasets for each student: one dataset per student for the bar chart
    datasets = []
    # List of colors for bars (will cycle if there are more students)
    colors = ["#4A90E2", "#50E3C2", "#F5A623", "#9013FE", "#D0021B", "#B8E986"]
    for i, (student, day_hours) in enumerate(data.items()):
        dataset = {
            "label": student,
            "data": [day_hours.get(day, 0) for day in days],
            "backgroundColor": colors[i % len(colors)],
            "borderWidth": 1
        }
        datasets.append(dataset)

    return days, datasets