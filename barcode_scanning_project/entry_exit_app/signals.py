from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student
import barcode
from barcode.writer import ImageWriter
from django.core.files import File
from io import BytesIO

@receiver(post_save, sender=Student)
def generate_barcode(sender, instance, created, **kwargs):
        if created:
            Code128 = barcode.get_barcode_class('code128')
            barcode_data = Code128(str(instance.rollno), writer=ImageWriter())
            buffer = BytesIO()
            barcode_data.write(buffer)
            instance.barcode.save(f'{instance.rollno}.png', File(buffer), save=False)
            instance.save()