from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializers

from accounts.models import CustomUser


class ProfileViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
