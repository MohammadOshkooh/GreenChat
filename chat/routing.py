from django.urls import re_path, path

from .consumers import ChatConsumer

websocket_urlpatterns = (
    path('ws/chat/<room_name>/<link>/', ChatConsumer.as_asgi()),
)
