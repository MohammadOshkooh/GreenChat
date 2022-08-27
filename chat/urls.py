from django.urls import path, include

from chat.views import chat

app_name = 'chat'

urlpatterns = [
    path('api/', include('chat.api.urls')),
    path('', chat, name='chat'),
]
