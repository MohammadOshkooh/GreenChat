from django.contrib.admindocs.views import ModelDetailView
from rest_framework.viewsets import ModelViewSet

from chat.models import Message
from chat.api.serializers import MessageSerializers


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers
