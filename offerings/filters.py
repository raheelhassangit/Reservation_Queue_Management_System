import django_filters
from .models import Offering


class OfferingFilter(django_filters.FilterSet):
    min_seats = django_filters.NumberFilter(field_name="available_count", lookup_expr="gte")
    organization = django_filters.NumberFilter(field_name="organization_id")

    class Meta:
        model = Offering
        fields = ["category", "organization"]