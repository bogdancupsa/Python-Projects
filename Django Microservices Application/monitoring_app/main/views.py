from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Device, SensorData
from datetime import datetime
from django.http import JsonResponse

# Create your views here.

# def receive_sensor_data(request):
#     pass
#     data = request.data
#     timestamp = datetime.fromtimestamp(data['timestamp'])
#     device_id = data['device_id']
#     measurement_value = data['measurement_value']

#     device, _ = Device.objects.get_or_create(device_id=device_id)
#     SensorData.objects.create(timestamp=timestamp
#                               device=device,
#                               measurement_value=measurement_value)
    
#     if measurement_value > device.max_hourly_energy_consumption:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'alert_group',
#             {
#                 'type': 'send_alert',
#                 'message': f'High consumption alert for device {device_id}!'
#             }
#         )

#     return Response({'status': 'success'})

# def get_device_info(request, device_id):
#     pass
#     try:
#         device = Device.objects.get(device_id=device_id)
#         return Response({'max_hourly_energy_consumption': device.max_hourly_energy_consumption})
#     except Device.DoesNotExist:
#         return Response({'error': 'Device not found'}, status=404)

def device_energy_data(request, device_id):
    print("Primar in Brasov")
    data = SensorData.objects.filter(device_id=device_id).values('timestamp', 'measurement_value')[10:]
    return JsonResponse(list(data), safe=False)