from celery import shared_task
from django.utils import timezone
from notifications.models import Notification
from .models import Waitlist
from offerings.models import Offering, Seat

@shared_task
def process_waitlist_task(offering_id):
    try:
        offering = Offering.objects.get(id=offering_id)
    except Offering.DoesNotExist:
        return "Offering not found"

    available = offering.seats.filter(status=Seat.Status.AVAILABLE).count()
    entries = Waitlist.objects.filter(offering=offering, notified_at__isnull=True).order_by("created_at")

    notified = 0
    for entry in entries:
        if available < entry.seats_wanted:
            break
        Notification.objects.create(
            user=entry.customer,
            message=f'Seats are now available for "{offering.name}" ({entry.seats_wanted} requested).',
            link=f"/offerings/{offering.id}/",
        )
        entry.notified_at = timezone.now()
        entry.save(update_fields=["notified_at"])
        available -= entry.seats_wanted
        notified += 1

    return f"Notified {notified} waitlist entries for offering {offering_id}"


@shared_task
def release_expired_holds():
    now = timezone.now()
    offering_ids = set(
        Seat.objects.filter(status=Seat.Status.RESERVED, held_until__lte=now)
        .values_list("offering_id", flat=True)
    )
    updated = Seat.objects.filter(
        status=Seat.Status.RESERVED, held_until__lte=now
    ).update(status=Seat.Status.AVAILABLE, held_by=None, held_until=None)

    for offering_id in offering_ids:
        process_waitlist_task.delay(offering_id)

    return f"Released {updated} expired seat holds, checked {len(offering_ids)} offerings"