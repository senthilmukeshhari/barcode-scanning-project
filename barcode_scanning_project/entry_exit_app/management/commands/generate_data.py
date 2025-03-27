from django.core.management.base import BaseCommand
from ...utils import generate_departments, generate_students

class Command(BaseCommand):

    help = 'Generate data for the application'

    def handle(self, *args, **options):
        generate_departments()
        print('Departments Data generated successfully')
        generate_students(27)
        print('Students Data generated successfully')