from django.urls import path

from chat.views import Index

app_name = 'chat'

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
