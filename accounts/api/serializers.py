from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import CustomUser


class UserSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='username')
    pic = serializers.ImageField(source='image')

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'pic']

