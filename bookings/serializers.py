from django.db import transaction
from rest_framework import serializers
from offerings.models import Offering, Seat
from .models import Booking, BookingSeat


class BookingCreateSerializer(serializers.Serializer):
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

    def create(self, validated_data):
        offering = validated_data["offering"]
        seat_ids = validated_data["seat_ids"]
        customer = self.context["request"].user

        with transaction.atomic():
            seats = list(
                Seat.objects.select_for_update()
                .filter(id__in=seat_ids, offering=offering)
                .order_by("id")
            )
            if len(seats) != len(seat_ids):
                raise serializers.ValidationError("Some seats don't exist in this offering.")
            if any(s.status != Seat.Status.AVAILABLE for s in seats):
                raise serializers.ValidationError("One or more seats are no longer available.")
            
            Seat.objects.filter(id__in=seat_ids).update(status=Seat.Status.BOOKED)
            booking = Booking.objects.create(customer=customer, offering=offering)
            BookingSeat.objects.bulk_create(
                [BookingSeat(booking=booking, seat=s) for s in seats]
            )
        return booking


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