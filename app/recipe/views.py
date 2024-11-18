"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import isAuthenticated

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializers_class = serializers.RecipeSerializer
    queryset = Recipe.object.all() # queryset = objects available in this view.
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAuthenticated]
