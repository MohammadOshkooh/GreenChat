from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerializers

from accounts.models import Profile


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
