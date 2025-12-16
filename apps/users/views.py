from django.http import Http404
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import IsAdminOrReadOnly

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    - Admins → can create users
    - Others → read-only
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]


class LoginView(TokenObtainPairView):
    """
    API endpoint for JWT authentication.
    Returns access and refresh tokens.
    """

    permission_classes = [permissions.AllowAny]


class UserAPIView(APIView):
    """
    API endpoint to:
    - GET /users/       → List all users
    - GET /users/<id>/  → Retrieve a specific user
    """

    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404("User not found")

    def get(self, request, pk=None, *args, **kwargs):
        if pk:  # Single user
            user = self.get_object(pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:  # List all users
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
