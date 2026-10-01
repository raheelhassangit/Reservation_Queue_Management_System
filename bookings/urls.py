from django.urls import path
from .views import BookingListView, HoldSeatsView, ConfirmBookingView, BookingDetailView
from .views import BookingListView, HoldSeatsView, ConfirmBookingView, ReleaseHoldView

urlpatterns = [
    path("", BookingListView.as_view(), name="booking-list"),
    path("hold/", HoldSeatsView.as_view(), name="booking-hold"),
    path("confirm/", ConfirmBookingView.as_view(), name="booking-confirm"),
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
]