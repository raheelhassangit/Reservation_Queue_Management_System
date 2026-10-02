from django.urls import path
from .views import BookingListView, HoldSeatsView, ConfirmBookingView, BookingDetailView
from .views import BookingListView, HoldSeatsView, ConfirmBookingView, ReleaseHoldView
from .views import JoinWaitlistView, MyWaitlistView, LeaveWaitlistView

urlpatterns = [
    path("", BookingListView.as_view(), name="booking-list"),
    path("hold/", HoldSeatsView.as_view(), name="booking-hold"),
    path("confirm/", ConfirmBookingView.as_view(), name="booking-confirm"),
    path("release/", ReleaseHoldView.as_view(), name="booking-release"),
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("waitlist/", JoinWaitlistView.as_view(), name="waitlist-join"),
    path("waitlist/mine/", MyWaitlistView.as_view(), name="waitlist-mine"),
    path("waitlist/<int:pk>/leave/", LeaveWaitlistView.as_view(), name="waitlist-leave"),
]