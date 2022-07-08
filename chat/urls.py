from django.urls import path

from chat.views import Chat

app_name = 'chat'

urlpatterns = [
    path('<room_name>/', Chat.as_view(), name='chat'),
]
