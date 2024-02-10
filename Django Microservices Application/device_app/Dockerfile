FROM python:3.10

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY ./device_app/device_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pika

COPY . .

EXPOSE 8012

CMD ["python", "manage.py", "runserver", "0.0.0.0:8012"]

