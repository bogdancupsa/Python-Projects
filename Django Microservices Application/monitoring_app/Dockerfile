FROM python:3.10

ENV PYTHONBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=monitoring_app.settings

WORKDIR /code

COPY ./monitoring_app/monitoring_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pika

COPY . .

EXPOSE 8036

CMD ["daphne", "-b", "0.0.0.0", "-p", "8036", "monitoring_app.asgi:application"]