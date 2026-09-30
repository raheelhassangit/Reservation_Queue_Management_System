from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking
from .serializers import BookingSerializer, SeatSelectionSerializer
from .services import confirm_booking, hold_seats
from .services import confirm_booking, hold_seats, release_hold


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return (
            Booking.objects.filter(customer=self.request.user)
            .select_related("offering")
            .prefetch_related("booked_seats__seat")
        )


class HoldSeatsView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        s = SeatSelectionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        until = hold_seats(
            request.user, s.validated_data["offering"], s.validated_data["seat_ids"]
        )
        return Response({"seat_ids": s.validated_data["seat_ids"], "held_until": until})


class ConfirmBookingView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        s = SeatSelectionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        booking = confirm_booking(
            request.user, s.validated_data["offering"], s.validated_data["seat_ids"]
        )
        return Response(BookingSerializer(booking).data, status=201)
    
    
class ReleaseHoldView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        s = SeatSelectionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        released = release_hold(
            request.user, s.validated_data["offering"], s.validated_data["seat_ids"]
        )
        return Response({"released": released})    