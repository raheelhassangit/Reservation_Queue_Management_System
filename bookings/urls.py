from django.urls import path
from .views import BookingListView, HoldSeatsView, ConfirmBookingView

urlpatterns = [
    path("", BookingListView.as_view(), name="booking-list"),
    path("hold/", HoldSeatsView.as_view(), name="booking-hold"),
    path("confirm/", ConfirmBookingView.as_view(), name="booking-confirm"),
]