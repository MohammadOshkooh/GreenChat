from rest_framework import serializers
from .models import Message


class ChatSerializersWithoutImage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__', 'content', 'created']


class ChatSerializersWithImage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__', 'image', 'created']
