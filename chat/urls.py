from django.urls import path

from chat.views import ChatView, Index

app_name = 'chat'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<room_name>/', ChatView.as_view(), name='chat'),
]
