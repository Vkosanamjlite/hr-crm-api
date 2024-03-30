"""
User views module for CRM API
"""

from rest_framework import generics, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import (
    UserCreateSerializer,
    AuthTokenSerializer
)


class UserList(generics.ListAPIView):
    serializer_class = UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

    def create(self, request, *args, **kwargs):
        response = super(UserCreateAPIView,
                         self).create(request,
                                      *args,
                                      **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Ensure we have a valid user instance from the serializer
            user = self.get_serializer().instance
            if user and user.pk:
                token, created = Token.objects.get_or_create(user=user)
                response.data['token'] = token.key
            else:
                pass
        return response


class CreateTokenView(generics.CreateAPIView):
    """ Create a new auth token for user """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key}, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Retrieve and update the authenticated user """
        return self.request.user
