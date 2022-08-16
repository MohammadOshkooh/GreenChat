from django.urls import path, include

from .views import MessageViewSet, ChatViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('message', MessageViewSet)
router.register('chat', ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
