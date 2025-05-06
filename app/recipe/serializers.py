"""
Serializers for our recipe model
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag
)


class RecipeModelSerializer(serializers.ModelSerializer):
    """Serializers for recipe"""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeModelSerializer):
    """Serializer for the recipe detail"""

    class Meta(RecipeModelSerializer.Meta):
        fields = RecipeModelSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
