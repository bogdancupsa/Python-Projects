from django.urls import path
from . import views

urlpatterns = [
    path('graph/<int:device_id>/', views.device_energy_data, name='device-energy-data'),
]