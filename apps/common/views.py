from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .backend import JWTAuthentication

from .renderers import UserJSONRenderer
from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer
)

from django.contrib.auth.hashers import check_password
from .models import User

auth = JWTAuthentication()   


class SignUpAPIView(CreateAPIView):
    """Register a new user."""
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class SignInAPIView(CreateAPIView):
    """Login a registered user."""
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    