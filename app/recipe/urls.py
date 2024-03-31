""" URL Configuration for recipe app """
from django.urls import (
    path,
    include,
)
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'recipe'

router = DefaultRouter()
router.register(r'recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
]
