from django.urls import re_path, path

from .consumers import ChatConsumer

websocket_urlpatterns = (
    # re_path(r'ws/chat/(?P<room_name>\w+)/$(?P<link>/w+)/$', ChatConsumer.as_asgi()),
    path('wss/chat/<room_name>/<link>/', ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
)
