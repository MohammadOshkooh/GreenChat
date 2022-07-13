from django.urls import path

from chat.views import ChatView, index

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/<str:link>', ChatView.as_view(), name='chat'),
]
