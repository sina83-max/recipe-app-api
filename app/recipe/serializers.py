"""
Serializers for our recipe model
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeModelSerializer(serializers.ModelSerializer):
    """Serializers for recipe"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Serializer for the recipe detail"""

    class Meta(RecipeModelSerializer.Meta):
        fields = RecipeModelSerializer.Meta.fields + ['description']
