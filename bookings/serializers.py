from django.db import transaction
from rest_framework import serializers
from offerings.models import Offering, Seat
from .models import Booking, BookingSeat, Waitlist


class BookingSerializer(serializers.ModelSerializer):
    offering_name = serializers.CharField(source="offering.name", read_only=True)
    offering_active = serializers.BooleanField(source="offering.is_active", read_only=True)
    seats = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ["id", "offering", "offering_name", "offering_active", "seats", "total_price", "created_at"]

    def get_seats(self, obj):
        return [bs.seat.seat_number for bs in obj.booked_seats.all()]

    def get_total_price(self, obj):
        return obj.offering.price * obj.booked_seats.count()
    
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
    
class JoinWaitlistSerializer(serializers.Serializer):
    offering = serializers.PrimaryKeyRelatedField(queryset=Offering.objects.all())
    seats_wanted = serializers.IntegerField(min_value=1, default=1)

class WaitlistSerializer(serializers.ModelSerializer):
    offering_name = serializers.CharField(source="offering.name", read_only=True)
    class Meta:
        model = Waitlist
        fields = ["id", "offering", "offering_name", "seats_wanted", "created_at", "notified_at"]    