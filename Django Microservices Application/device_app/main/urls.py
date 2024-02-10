from django.urls import path

from . import views

urlpatterns = [
    path('get_all_devices/', views.get_all_devices, name='get_all_devices'),
    path('get_user_devices/<int:user_id>/', views.get_user_devices, name='get_user_devices'),
    path('add_device/', views.add_device, name='add_device'),
    path('edit_device/<int:device_id>/', views.edit_device, name='edit_device'),
    path('delete_device/<int:device_id>/', views.delete_device, name='delete_device'),
    path('delete_devices_by_id/<int:client_id>/', views.delete_devices_by_id, name='delete_devices_by_id'),
]
