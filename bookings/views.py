from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"


class BookingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return (
            Booking.objects.filter(customer=self.request.user)
            .select_related("offering")
            .prefetch_related("booked_seats__seat")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookingCreateSerializer
        return BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(BookingSerializer(booking).data, status=201)