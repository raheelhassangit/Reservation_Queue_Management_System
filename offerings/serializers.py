from rest_framework import serializers
from .models import Offering, Seat

class OfferingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offering
        fields = ["id", "name", "category", "custom_category", "total_seats", "max_seats_per_booking"]

    def validate(self, data):
        if data.get("category") == Offering.Category.OTHER and not data.get("custom_category"):
            raise serializers.ValidationError(
                {"custom_category": "This field is required when category is 'other'."}
            )
        if data.get("category") != Offering.Category.OTHER:
            data["custom_category"] = ""  # ignore stray value if category isn't "other"
        return data

    def create(self, validated_data):
        organization = self.context["request"].user.organization
        offering = Offering.objects.create(organization=organization, **validated_data)
        seats = [
            Seat(offering=offering, seat_number=str(i))
            for i in range(1, offering.total_seats + 1)
        ]
        Seat.objects.bulk_create(seats)
        return offering