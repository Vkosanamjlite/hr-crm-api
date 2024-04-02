from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

app_name = 'contact'  # Define the app name here

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]
