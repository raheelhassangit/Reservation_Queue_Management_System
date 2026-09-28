from django.db.models import Count, Q
from rest_framework import generics, permissions
from .models import Offering
from .serializers import (
    OfferingCreateSerializer,
    OfferingListSerializer,
    OfferingDetailSerializer,
)
from django.utils import timezone

class IsProvider(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"


def offerings_queryset():
    now = timezone.now()
    return Offering.objects.select_related("organization").annotate(
        available_count=Count(
            "seats",
            filter=Q(seats__status="available")
            | Q(seats__status="reserved", seats__held_until__lte=now),
        )
    )


class OfferingListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return offerings_queryset()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferingCreateSerializer
        return OfferingListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsProvider()]
        return [permissions.AllowAny()]


class OfferingDetailView(generics.RetrieveAPIView):
    serializer_class = OfferingDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return offerings_queryset().prefetch_related("seats")