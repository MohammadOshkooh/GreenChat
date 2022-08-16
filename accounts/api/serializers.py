from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Profile


class ProfileSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='user')
    id = serializers.IntegerField(source='user.id')
    pic = serializers.ImageField(source='image')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'pic']
