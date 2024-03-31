""" Views for the recipes app """

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from .serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """ View set for the recipes app  """
    serializer_class = RecipeDetailsSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Return all recipes for the user """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return serializer class for the """
        if self.action == 'list':
            return RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new recipe and return """
        serializer.save(user=self.request.user)
