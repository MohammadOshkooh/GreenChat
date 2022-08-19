from django.contrib.admindocs.views import ModelDetailView
from rest_framework.viewsets import ModelViewSet

from chat.models import Message, Chat, ContactList
from chat.api.serializers import MessageSerializers, ChatSerializers, ContactListSerializers


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializers


class ContactListViewSet(ModelViewSet):
    queryset = ContactList.objects.all()
    serializer_class = ContactListSerializers
