# bookings/urls.py
from django.urls import path
from .views import BookingListCreateView

urlpatterns = [path("", BookingListCreateView.as_view(), name="booking-list-create")]