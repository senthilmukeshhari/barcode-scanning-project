from django.core.management.base import BaseCommand
from ...utils import generate_departments, generate_students, generate_labs

class Command(BaseCommand):

    help = 'Generate data for the application'

    def handle(self, *args, **options):
        generate_departments()
        print('Departments Data generated successfully')

        generate_students(222703100, 28, 1, 'A', 2022)
        print('BCA III Year A Section Students Data generated successfully')
        generate_students(222703200, 26, 1, 'B', 2022)
        print('BCA III Year B Section Students Data generated successfully')

        generate_students(232703100, 23, 1, 'A', 2023)
        print('BCA II Year A Section Students Data generated successfully')

        generate_students(242703100, 20, 1, 'A', 2024)
        print('BCA I Year A Section Students Data generated successfully')

        generate_labs()
        print('Lab Datagenerate successfully')