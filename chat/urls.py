from django.urls import path

from chat.views import Chat

app_name = 'chat'

urlpatterns = [
    path('', Chat.as_view(), name='index'),
]
