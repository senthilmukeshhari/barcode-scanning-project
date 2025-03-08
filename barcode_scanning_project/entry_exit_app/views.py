from django.shortcuts import render, get_object_or_404
from entry_exit_app.models import EntryExit, Student, Department
from django.utils.timezone import now
from django.http import JsonResponse
import json

def get_status_and_users_in_lab():
    today = now().date()
    students = EntryExit.objects.filter(entry_time__date=today,  exit_time__isnull=True)
    students_in_lab = EntryExit.objects.filter(entry_time__date=today).count()
    lab_status =f'There are {students.count()} user(s) in the lab.' if students.count() > 0 else 'No one in the lab currently.'
    return students_in_lab, lab_status

def get_initial_notifications():
    today = now().date()
    entries = EntryExit.objects.filter(entry_time__date=today).order_by('-entry_time')
    notifications = []
    for entry in entries:
        if entry.exit_time:
            notifications.append(f"User {entry.student.rollno} exited the lab.")
        notifications.append(f"User {entry.student.rollno} entered the lab.")
    return notifications

def context_data():
    students_in_lab, lab_status = get_status_and_users_in_lab()
    notifications = get_initial_notifications()
    context = {
        'website_name' : 'College Lab Entry/Exit System',
        'students_in_lab' : students_in_lab,
        'lab_status': lab_status,
        'notifications': notifications
    }
    return context
    
def home(request):
    context = context_data()
    return render(request, 'home.html', context=context)

def update_context_with_student_data(context, entry_exit_log, status):
    context['student'] = entry_exit_log.student.rollno
    context['student_name'] = entry_exit_log.student.name
    context['department'] = entry_exit_log.student.department.name
    context['section'] = entry_exit_log.student.section
    context['profile_image'] = entry_exit_log.student.profile_image.url
    context['entry_time'] = entry_exit_log.entry_time.strftime('%Y-%m-%d %H:%M:%S') if status == 'entry' else None
    context['exit_time'] = entry_exit_log.exit_time.strftime('%Y-%m-%d %H:%M:%S') if status == 'exit' else None
    context['students_in_lab'], context['lab_status'] = get_status_and_users_in_lab()
    context['notification'] = f"User {entry_exit_log.student.rollno} {status}ed the lab."

def scan_barcode(request):
    context = context_data()
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            barcode = data['barcode']
            student = get_object_or_404(Student, rollno=barcode, is_active=True)

            open_log = EntryExit.objects.filter(student=student, exit_time__isnull=True).first()
            if open_log:
                open_log.exit_time = now()
                open_log.save()
                update_context_with_student_data(context, open_log, 'exit')
                return JsonResponse({
                    'status': 'exit',
                    'message': 'Exit logged successfully.',
                    'data': context
                }, status=201)

            new_entry = EntryExit.objects.create(student=student, entry_time=now())
            update_context_with_student_data(context, new_entry, 'entry')
            return JsonResponse({
                'status': 'entry',
                'message': 'Entry logged successfully.',
                'data': context
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Student.DoesNotExist as s:
            print('Does not : ', s)
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid barcode'
            }, status=400)
        except Exception as e:
            print('error : ', e)
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid barcode' + barcode + ' or student is inactive.'
            }, status=400)