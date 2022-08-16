from django.urls import path, include
from rest_framework import routers
from .views import ProfileViewSet

router = routers.SimpleRouter()

router.register('', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls))
]
