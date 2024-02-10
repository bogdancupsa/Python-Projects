from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Device
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .perm_file import IsAdminUser
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
import jwt
import json

@api_view(['GET'])
# @permission_classes([IsAdminUser])
def get_all_devices(request):                                                                                                                                                                                                            
    auth_token = request.headers.get('Authorization').split()[1]
    auth = JWTAuthentication()
    decoded_data = jwt.decode(auth_token, "5ahp8kseKOVB_w", algorithms="HS256")
    print(decoded_data)                                                                                                                                                                                       

    if decoded_data['user_id'] != 1:
        print("nu esti admin")
        return JsonResponse({'error': 'Forbidden'}, status=403)
    else:
        if request.method ==  'GET':
            devices = Device.objects.all()
            
            device_list = [
                {
                    'id': device.id,
                    'client_id': device.client_id,
                    'description': device.description,
                    'address': device.address,
                    'max_hourly_energy_consumption': device.max_hourly_energy_consumption            
                }
                for device in devices
            ]

            return JsonResponse({'devices': device_list}, status=200)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_user_devices(request, user_id):
    devices = Device.objects.filter(client_id=user_id)
    print(request.body)

    device_list = [
        {
            'id': device.id,
            'client_id': device.client_id,
            'description': device.description,
            'address': device.address,
            'max_hourly_energy_consumption': device.max_hourly_energy_consumption            
        }
        for device in devices
    ]

    return JsonResponse({'devices': device_list}, status=200)

@api_view(['POST'])
# @permission_classes([IsAdminUser])
def add_device(request):
    auth_token = request.headers.get('Authorization').split()[1]
    auth = JWTAuthentication()
    decoded_data = jwt.decode(auth_token, "5ahp8kseKOVB_w", algorithms="HS256")
    print(decoded_data)  
    print(request.headers)

    user_role = request.headers.get('X-User-Role')

    if decoded_data['user_id'] != 1:
        print("   ")
        return JsonResponse({'error': 'Forbidden'}, status=403)
    else:
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                device = Device(
                    client_id=data['client_id'],
                    description=data['description'], 
                    address=data['address'], 
                    max_hourly_energy_consumption=data['max_hourly_energy_consumption']
                )
                device.save()

                return JsonResponse({'status': 'Device added successfully'}, status=201)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format in the request body'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def edit_device(request, device_id):

    auth_token = request.headers.get('Authorization').split()[1]
    auth = JWTAuthentication()
    decoded_data = jwt.decode(auth_token, "5ahp8kseKOVB_w", algorithms="HS256")

    user_role = request.headers.get('X-User-Role')
    if decoded_data['user_id'] != 1:
        print("   ")
        return JsonResponse({'error': 'Forbidden'}, status=403)
    else:
        print(request.headers)
        device = get_object_or_404(Device, id=device_id)
        if request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            device.description = data['description']
            device.address = data['address']
            device.max_hourly_energy_consumption = data['max_hourly_energy_consumption']
            device.save()
            return JsonResponse({'status': 'Device edited successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['DELETE'])
# @permission_classes([IsAdminUser])
def delete_device(request, device_id):

    auth_token = request.headers.get('Authorization').split()[1]
    auth = JWTAuthentication()
    decoded_data = jwt.decode(auth_token, "5ahp8kseKOVB_w", algorithms="HS256")

    print(request.headers)
    user_role = request.headers.get('X-User-Role')
    if decoded_data['user_id'] != 1:
        print("     ")
        return JsonResponse({'error': 'Forbidden'}, status=403)
    else:
        device = get_object_or_404(Device, id=device_id)
        device.delete()
        return JsonResponse({'status': 'Device deleted successfully'}, status=200)

@csrf_exempt
def delete_devices_by_id(request, client_id):
    user_role = request.headers.get('X-User-Role')
    if decoded_data['user_id'] != 1:
        print("   ")
        return JsonResponse({'error': 'Forbidden'}, status=403)
    else:
        devices = Device.objects.filter(client_id=client_id)
        print(devices)
        devices.delete()
        return JsonResponse({'status': 'Devices deleted successfully'}, status=200)