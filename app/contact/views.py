from rest_framework import viewsets, permissions
from core.models import Contact
from .serializers import ContactSerializer
from rest_framework.authentication import TokenAuthentication


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]  # Updated to IsAuthenticated

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
