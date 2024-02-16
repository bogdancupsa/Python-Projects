from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import MonitoringConsumer

websocket_urlpatterns = [
    path('ws/monitoring/', MonitoringConsumer.as_asgi()),
]
