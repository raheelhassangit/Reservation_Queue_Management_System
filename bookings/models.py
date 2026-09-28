from django.conf import settings
from django.db import models
from offerings.models import Offering, Seat


class Booking(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    offering = models.ForeignKey(
        Offering, on_delete=models.CASCADE, related_name="bookings"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="booked_seats"
    )
    seat = models.OneToOneField(Seat, on_delete=models.PROTECT, related_name="booking_seat")