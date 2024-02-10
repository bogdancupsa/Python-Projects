FROM python:3.10

ENV PYTHONBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=chat_app.settings

WORKDIR /code

COPY ./chat_app/chat_app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8024

CMD ["daphne", "-b", "0.0.0.0", "-p", "8024", "chat_app.asgi:application"]