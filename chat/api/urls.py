from django.urls import path, include

from .views import MessageViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('', MessageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
