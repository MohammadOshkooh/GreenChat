from rest_framework import serializers

from chat.models import Message, Chat


class MessageSerializers(serializers.ModelSerializer):
    recvId = serializers.IntegerField(source='related_chat.id')
    recvIsGroup = serializers.BooleanField(source='Received_from_the_group')

    class Meta:
        model = Message
        fields = ['id', '__str__', 'sender', 'body', 'time', 'status', 'recvId', 'recvIsGroup', 'contain_image',
                  'image']


class ChatSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='room_name')
    pic = serializers.ImageField(source='image')

    class Meta:
        model = Chat
        fields = ['id', 'name', 'members', 'pic', 'owner', 'link']
