from django.contrib import admin
from .models import Booking, BookingSeat


class BookingSeatInline(admin.TabularInline):
    model = BookingSeat
    extra = 0
    raw_id_fields = ("seat",)
    readonly_fields = ("seat_id_display", "seat_number_display")
    fields = ("seat", "seat_id_display", "seat_number_display")

    def seat_id_display(self, obj):
        return obj.seat_id

    def seat_number_display(self, obj):
        return obj.seat.seat_number


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "offering", "seats_booked", "created_at")
    list_filter = ("offering", "created_at")
    search_fields = ("customer__username", "offering__name")
    list_select_related = ("customer", "offering")
    inlines = [BookingSeatInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("booked_seats__seat")

    def seats_booked(self, obj):
        return ", ".join(
            f"#{bs.seat_id} ({bs.seat.seat_number})" for bs in obj.booked_seats.all()
        )