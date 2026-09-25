from rest_framework import generics, permissions
from .serializers import CustomerRegisterSerializer, ProviderRegisterSerializer


class CustomerRegisterView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProviderRegisterView(generics.CreateAPIView):
    serializer_class = ProviderRegisterSerializer
    permission_classes = [permissions.AllowAny]