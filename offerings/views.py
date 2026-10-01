from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import OfferingFilter
from .models import Offering
from .permissions import IsProvider, IsOfferingOwner
from .serializers import (
    OfferingCreateSerializer,
    OfferingListSerializer,
    OfferingDetailSerializer,
    OfferingUpdateSerializer,
)


def offerings_queryset():
    now = timezone.now()

    return Offering.objects.filter(
        is_active=True
    ).select_related(
        "organization"
    ).annotate(
        available_count=Count(
            "seats",
            filter=(
                Q(seats__status="available")
                | Q(
                    seats__status="reserved",
                    seats__held_until__lte=now
                )
            ),
        )
    )


class OfferingListCreateView(generics.ListCreateAPIView):
    filterset_class = OfferingFilter
    search_fields = ["name", "organization__name"]
    ordering_fields = ["total_seats", "created_at", "available_count"]
    ordering = ["-created_at"]

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


class OfferingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = offerings_queryset().prefetch_related("seats")

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]

        return [IsProvider(), IsOfferingOwner()]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return OfferingUpdateSerializer

        return OfferingDetailSerializer


class MyOfferingsView(generics.ListAPIView):
    serializer_class = OfferingListSerializer
    permission_classes = [IsProvider]

    filterset_class = OfferingFilter
    search_fields = ["name"]
    ordering_fields = ["total_seats", "created_at", "available_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        now = timezone.now()

        return Offering.objects.filter(
            organization=self.request.user.organization
        ).annotate(
            available_count=Count(
                "seats",
                filter=(
                    Q(seats__status="available")
                    | Q(
                        seats__status="reserved",
                        seats__held_until__lte=now
                    )
                ),
            )
        )


class ArchiveOfferingView(APIView):
    permission_classes = [IsProvider, IsOfferingOwner]

    def post(self, request, pk):
        offering = get_object_or_404(
            Offering,
            pk=pk
        )

        self.check_object_permissions(
            request,
            offering
        )

        offering.is_active = not offering.is_active

        offering.save(
            update_fields=["is_active"]
        )

        return Response({
            "is_active": offering.is_active
        })