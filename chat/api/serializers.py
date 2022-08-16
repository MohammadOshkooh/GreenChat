from rest_framework import serializers

from chat.models import Message


class MessageSerializers(serializers.ModelSerializer):
    recvId = serializers.IntegerField(source='related_chat.id')
    recvIsGroup = serializers.BooleanField(source='Received_from_the_group')

    class Meta:
        model = Message
        fields = ['id', '__str__', 'sender', 'body', 'time', 'status', 'recvId', 'recvIsGroup']
