from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from offerings.models import Seat
from .models import Booking, BookingSeat


def _lock_seats(offering, seat_ids):
    seats = list(
        Seat.objects.select_for_update()
        .filter(id__in=seat_ids, offering=offering)
        .order_by("id")
    )
    if len(seats) != len(set(seat_ids)):
        raise ValidationError("Some seats don't exist in this offering.")
    return seats


def hold_seats(user, offering, seat_ids):
    with transaction.atomic():
        seats = _lock_seats(offering, seat_ids)
        if not all(s.is_takeable() for s in seats):
            raise ValidationError("One or more seats are no longer available.")

        until = timezone.now() + timedelta(minutes=settings.SEAT_HOLD_MINUTES)
        Seat.objects.filter(id__in=[s.id for s in seats]).update(
            status=Seat.Status.RESERVED, held_by=user, held_until=until
        )
    return until


def confirm_booking(user, offering, seat_ids):
    with transaction.atomic():
        seats = _lock_seats(offering, seat_ids)
        now = timezone.now()
        for s in seats:
            if (
                s.status != Seat.Status.RESERVED
                or s.held_by_id != user.id
                or s.held_until <= now
            ):
                raise ValidationError(
                    "Your hold on one or more seats is missing or has expired."
                )

        Seat.objects.filter(id__in=[s.id for s in seats]).update(
            status=Seat.Status.BOOKED, held_by=None, held_until=None
        )
        booking = Booking.objects.create(customer=user, offering=offering)
        BookingSeat.objects.bulk_create(
            [BookingSeat(booking=booking, seat=s) for s in seats]
        )
    return booking

def release_hold(user, offering, seat_ids):
    with transaction.atomic():
        seats = _lock_seats(offering, seat_ids)
        to_release = [
            s for s in seats
            if s.status == Seat.Status.RESERVED and s.held_by_id == user.id
        ]
        Seat.objects.filter(id__in=[s.id for s in to_release]).update(
            status=Seat.Status.AVAILABLE, held_by=None, held_until=None
        )
    return len(to_release)