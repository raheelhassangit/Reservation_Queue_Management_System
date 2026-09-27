from rest_framework import generics, permissions
from .models import Offering
from .serializers import OfferingCreateSerializer


class IsProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"


class OfferingCreateView(generics.CreateAPIView):
    serializer_class = OfferingCreateSerializer
    permission_classes = [IsProvider]