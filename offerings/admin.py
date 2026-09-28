from django.contrib import admin
from .models import Offering, Seat


@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "category", "total_seats", "max_seats_per_booking")
    list_filter = ("category", "organization")
    search_fields = ("name", "organization__name")
    list_select_related = ("organization",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "seat_number", "offering", "status", "held_by", "held_until")
    list_filter = ("offering", "status")
    search_fields = ("id", "seat_number")
    list_select_related = ("offering",)
    ordering = ("id",)