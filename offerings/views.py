from django.db.models import Count, Q
from rest_framework import generics, permissions
from .models import Offering
from .serializers import (
    OfferingCreateSerializer,
    OfferingListSerializer,
    OfferingDetailSerializer,
)


class IsProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"


def offerings_queryset():
    return Offering.objects.select_related("organization").annotate(
        available_count=Count("seats", filter=Q(seats__status="available"))
    )


class OfferingListCreateView(generics.ListCreateAPIView):
    queryset = offerings_queryset()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferingCreateSerializer
        return OfferingListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsProvider()]
        return [permissions.AllowAny()]


class OfferingDetailView(generics.RetrieveAPIView):
    queryset = offerings_queryset().prefetch_related("seats")
    serializer_class = OfferingDetailSerializer
    permission_classes = [permissions.AllowAny]