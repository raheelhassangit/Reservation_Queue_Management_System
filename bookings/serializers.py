from django.db import transaction
from rest_framework import serializers
from offerings.models import Offering, Seat
from .models import Booking, BookingSeat



class BookingSerializer(serializers.ModelSerializer):
    offering_name = serializers.CharField(source="offering.name", read_only=True)
    seats = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ["id", "offering", "offering_name", "seats", "created_at"]

    def get_seats(self, obj):
        return [bs.seat.seat_number for bs in obj.booked_seats.all()]
    
class SeatSelectionSerializer(serializers.Serializer):
    offering = serializers.PrimaryKeyRelatedField(queryset=Offering.objects.all())
    seat_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate(self, data):
        offering, seat_ids = data["offering"], data["seat_ids"]
        if len(set(seat_ids)) != len(seat_ids):
            raise serializers.ValidationError("Duplicate seats in request.")
        if len(seat_ids) > offering.max_seats_per_booking:
            raise serializers.ValidationError(
                f"You can book at most {offering.max_seats_per_booking} seat(s) at once."
            )
        return data    