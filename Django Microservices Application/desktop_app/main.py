import csv
import pika
import json
import time
import sys
import os
from datetime import datetime

max_retries = 20
wait_time = 40
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')

def send_to_rabbitmq(device_id, measurement_value, timestamp, channel):
    data = {
        "timestamp": timestamp,
        "device_id": device_id,
        "measurement_value": measurement_value,
    }
    channel.queue_declare(queue='sensor_data')
    channel.basic_publish(exchange='', routing_key='sensor_data', body=json.dumps(data))

def read_csv_and_send(filepath, device_id, channel):
    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file)
        timestamp = 1
        for index, row in enumerate(csv_reader, start=1):
            timestamp_new = datetime.now().isoformat()
            if (index + 1) % 6 == 0:
                measurement_value = float(row[0])
                send_to_rabbitmq(device_id,measurement_value, timestamp_new, channel)
                timestamp += 1

def main():
    connection_attempts = 0
    while connection_attempts < max_retries:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            channel = connection.channel()
            break
        except pika.exceptions.AMQPConnectionError:
            connection_attempts += 1
            time.sleep(wait_time)
    else:
        print("Failed to connect to RabbitMQ after several attempts.")
        sys.exit(1)

    try:
        read_csv_and_send('sensor.csv', 26, channel)
        time.sleep(60)
        read_csv_and_send('sensor.csv', 30, channel)
    finally:
        connection.close()

if __name__ == "__main__":
    main()

