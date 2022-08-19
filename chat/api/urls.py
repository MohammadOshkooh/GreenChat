from django.urls import path, include

from .views import MessageViewSet, ChatViewSet, ContactListViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('message', MessageViewSet)
router.register('chat', ChatViewSet)
router.register('contact-list', ContactListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
