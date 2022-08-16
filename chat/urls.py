from django.urls import path, include

from chat.views import chat_view, index, new

app_name = 'chat'

urlpatterns = [
    path('api/', include('chat.api.urls')),
    path('<str:room_name>/<str:link>', new, name='chat'),
    path('', index, name='index'),

    # path('<str:room_name>/<str:link>', chat_view, name='chat'),
]
