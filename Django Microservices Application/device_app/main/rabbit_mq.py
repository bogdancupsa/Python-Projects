import pika
import json
from .models import Device

def send_device_data_to_rabbitmq():
    devices = Device.objects.filter(id__in=[40, 41])

    for device in devices:
        data = {
            "device_id": device.id,
            "max_consumption": device.max_hourly_energy_consumption
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='max_consumption_data')

        channel.basic_publish(exchange='', routing_key='max_consumtpion_data', body=json.dumps(data))
        connection.close()

send_device_data_to_rabbitmq()