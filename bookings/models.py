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
    
    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username} - {self.offering.name}"


class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="booked_seats"
    )
    seat = models.OneToOneField(Seat, on_delete=models.PROTECT, related_name="booking_seat")
    
    def __str__(self):
        return f"{self.booking_id} -> {self.seat}"
    
class Waitlist(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="waitlist_entries")
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name="waitlist_entries")
    seats_wanted = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ["created_at"]
        unique_together = ("customer", "offering")    