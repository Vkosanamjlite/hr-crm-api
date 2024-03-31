"""
Serializers for recipes API
"""
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for recipe objects """

    class Meta:
        """
        Meta class is a subclass of Serializer.ModelSerializer which
        provides the necessary configurations for the serialization
        of Recipe model
        """

        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailsSerializer(RecipeSerializer):
    """ Serializer for recipe details """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
