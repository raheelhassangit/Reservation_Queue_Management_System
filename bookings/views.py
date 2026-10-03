from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, Waitlist
from .serializers import (
    BookingSerializer,
    SeatSelectionSerializer,
    JoinWaitlistSerializer,
    WaitlistSerializer,
)
from .services import confirm_booking, hold_seats, release_hold, join_waitlist
from .throttles import HoldRateThrottle
from django.db.models import Case, When, Value, IntegerField

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
            .annotate(
                offering_inactive=Case(
                    When(offering__is_active=False, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .order_by("offering_inactive", "-created_at")
        )


class HoldSeatsView(APIView):
    permission_classes = [IsCustomer]
    throttle_classes = [HoldRateThrottle]

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


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return (
            Booking.objects.filter(customer=self.request.user)
            .select_related("offering")
            .prefetch_related("booked_seats__seat")
        )


class ReleaseHoldView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        s = SeatSelectionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        released = release_hold(
            request.user, s.validated_data["offering"], s.validated_data["seat_ids"]
        )
        return Response({"released": released})


class JoinWaitlistView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        s = JoinWaitlistSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        entry = join_waitlist(request.user, s.validated_data["offering"], s.validated_data["seats_wanted"])
        return Response(WaitlistSerializer(entry).data, status=201)


class MyWaitlistView(generics.ListAPIView):
    serializer_class = WaitlistSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Waitlist.objects.filter(customer=self.request.user).select_related("offering")


class LeaveWaitlistView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, pk):
        Waitlist.objects.filter(id=pk, customer=request.user).delete()
        return Response({"ok": True})