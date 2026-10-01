from django.db import models
from organizations.models import Organization
from django.conf import settings
from django.utils import timezone

class Offering(models.Model):
    class Category(models.TextChoices):
        BUS = "bus", "Bus"
        COURSE = "course", "Course"
        EVENT = "event", "Event"
        APPOINTMENT = "appointment", "Appointment"
        OTHER = "other", "Other"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="offerings"
    )
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=15, choices=Category.choices)
    custom_category = models.CharField(max_length=50, blank=True)
    total_seats = models.PositiveIntegerField()
    max_seats_per_booking = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, blank=True, default="") 
    origin = models.CharField(max_length=150, blank=True, default="")     
    destination = models.CharField(max_length=150, blank=True, default="") 
    starts_at = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, default="")

    def display_category(self):
        return self.custom_category if self.category == self.Category.OTHER else self.get_category_display()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"
    
class Seat(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        BOOKED = "booked", "Booked"

    offering = models.ForeignKey(
        Offering, on_delete=models.CASCADE, related_name="seats"
    )
    seat_number = models.CharField(max_length=10)     # "A1", or just "17"
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.AVAILABLE
    )
    held_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="held_seats",
    )
    held_until = models.DateTimeField(null=True, blank=True)

    def is_hold_expired(self):
        return (
            self.status == self.Status.RESERVED
            and self.held_until is not None
            and self.held_until <= timezone.now()
        )

    def is_takeable(self):
        return self.status == self.Status.AVAILABLE or self.is_hold_expired()

    @property
    def effective_status(self):
        return self.Status.AVAILABLE if self.is_hold_expired() else self.status
    
    class Meta:
        unique_together = ("offering", "seat_number")

    def __str__(self):
        return f"{self.offering.name} - {self.seat_number}"    