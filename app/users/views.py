"""
Views for the user API
"""
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Crete a new employee in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated employee"""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieve and return user"""
        return self.request.user
