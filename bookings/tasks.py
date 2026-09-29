from celery import shared_task
from django.utils import timezone
from offerings.models import Seat


@shared_task
def release_expired_holds():
    now = timezone.now()
    updated = Seat.objects.filter(
        status=Seat.Status.RESERVED, held_until__lte=now
    ).update(status=Seat.Status.AVAILABLE, held_by=None, held_until=None)
    return f"Released {updated} expired seat holds"