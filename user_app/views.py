from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny


class UserCreate(generics.CreateAPIView):
    """API-endpoint to create new User object."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
