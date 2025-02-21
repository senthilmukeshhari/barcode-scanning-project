from django.urls import path
from entry_exit_app import views

urlpatterns = [  
    path('', views.home, name='home'),  
    path('scan_barcode/', views.scan_barcode, name='scan_barcode') 
]