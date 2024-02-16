import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_app.settings')
django.setup()

import pika
import json
import datetime
from main.models import Device, SensorData

try:
    from channels.layers import get_channel_layer
except Exception as e:
    print(f'{e} - asta e exceptia de la import')
from asgiref.sync import async_to_sync
from django.utils import timezone

def callback(ch, method, properties, body):
    if method.routing_key == 'sensor_data':
        data = json.loads(body)

        print(data)

        try:
            timestamp_str = data['timestamp']
            
            try:
                device_instance, created = Device.objects.get_or_create(device_id=data['device_id'])
            except Exception as e:
                print(f"error 1           {e}")

            try:
                timestamp = datetime.datetime.fromisoformat(timestamp_str)
                timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())
                SensorData.objects.create(
                    device=device_instance,
                    measurement_value=data['measurement_value'],
                    timestamp=timestamp
                )
            except Exception as e:
                print(f"error 2       {e}")

            device = Device.objects.get(device_id=data['device_id'])
            try: 
                if data['measurement_value'] > device.max_hourly_energy_consumption:
                    print("CUPSA_alert")
                    print("       "     + str(data['measurement_value']) +  "                        ")
                    print("       "     + str(device.max_hourly_energy_consumption) +  "                        ")
                    try:
                        send_alert(data['device_id'])
                    except Exception as e:
                        print(f'{e} - eroare cand chem functia de send alert')
            except Exception as e:
                print(f'{e}   -   eroare in if ul ala')

        except:
            return

    elif method.routing_key == 'max_consumption_data':
        data = json.loads(body)
        Device.objects.update_or_create(
            device_id=data['device_id'],
            defaults={'max_hourly_energy_consumption': data['max_consumption']}
        )

def send_alert(device_id):
    try:
        channel_layer = get_channel_layer()
    except Exception as e:
        print(f'{e} - asta e exception de la get_channel_layer')

    message = f"Alert! Device {device_id} exceeded energy consumption limit."
    try:
        async_to_sync(channel_layer.group_send)( 
            'alert_group',
            {
                'type': 'send_alert',
                'message': message,
                'device_id': device_id
            }
        )
    except Exception as e:
        print(f'{e}  --  de la async to sync')

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='sensor_data')
channel.queue_declare(queue='max_consumption_data')

channel.basic_consume(queue='sensor_data', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='max_consumption_data', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
