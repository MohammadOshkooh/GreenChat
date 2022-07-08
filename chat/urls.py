from django.urls import path

from chat.views import Chat, Index

app_name = 'chat'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<room_name>/', Chat.as_view(), name='chat'),
]
