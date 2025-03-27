"""
Views for the user API
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import (
    UserSerializer,
    AuthTokenSerializers,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create token for signed-in users"""
    serializer_class = AuthTokenSerializers
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
