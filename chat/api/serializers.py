from rest_framework import serializers

from chat.models import Message


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__', 'owner', 'content', 'created', 'id']
