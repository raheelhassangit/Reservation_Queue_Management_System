from django.db import models
from organizations.models import Organization

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

    class Meta:
        unique_together = ("offering", "seat_number")

    def __str__(self):
        return f"{self.offering.name} - {self.seat_number}"    