from rest_framework import generics, permissions
from .models import Offering
from .serializers import OfferingCreateSerializer
from .serializers import OfferingListSerializer, OfferingDetailSerializer


class IsProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"


class OfferingCreateView(generics.CreateAPIView):
    serializer_class = OfferingCreateSerializer
    permission_classes = [IsProvider]
    

class OfferingListView(generics.ListAPIView):
    queryset = Offering.objects.all()
    serializer_class = OfferingListSerializer
    permission_classes = [permissions.AllowAny]


class OfferingDetailView(generics.RetrieveAPIView):
    queryset = Offering.objects.all()
    serializer_class = OfferingDetailSerializer
    permission_classes = [permissions.AllowAny]    