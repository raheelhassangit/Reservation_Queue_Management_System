from rest_framework import serializers
from .models import Offering, Seat

class OfferingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offering
        fields = [
            "id", "name", "category", "custom_category",
            "total_seats", "max_seats_per_booking",
            "location", "origin", "destination", "starts_at", "price", "description",
        ]

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

class SeatSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="effective_status", read_only=True)
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "status"]


class OfferingListSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    category_display = serializers.CharField(source="display_category", read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Offering
        fields = [
            "id", "name", "category_display", "organization_name",
            "total_seats", "available_seats", "max_seats_per_booking",
            "location", "origin", "destination", "starts_at", "price",
        ]

    def get_available_seats(self, obj):
        if hasattr(obj, "available_count"):
            return obj.available_count
        return obj.seats.filter(status="available").count()


class OfferingDetailSerializer(OfferingListSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta(OfferingListSerializer.Meta):
        fields = OfferingListSerializer.Meta.fields + ["seats", "description"]    
        
class OfferingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offering
        fields = [
            "name", "category", "custom_category", "max_seats_per_booking",
            "location", "origin", "destination", "starts_at", "price", "description",
        ]

    def validate(self, data):
        category = data.get("category", getattr(self.instance, "category", None))
        custom = data.get("custom_category", getattr(self.instance, "custom_category", ""))
        if category == Offering.Category.OTHER and not custom:
            raise serializers.ValidationError(
                {"custom_category": "This field is required when category is 'other'."}
            )
        return data        