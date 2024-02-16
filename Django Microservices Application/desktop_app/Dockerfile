FROM python:3.10

WORKDIR /app

COPY main.py .
COPY sensor.csv .

RUN pip install pika

ENV RABBITMQ_HOST=rabbitmq

CMD ["python", "main.py"]