from rest_framework import serializers
from .models import Message


class ChatSerializersWithoutImage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__', 'content', 'created', 'contain_image']


class ChatSerializersWithImage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['__str__', 'image', 'created', 'contain_image']
