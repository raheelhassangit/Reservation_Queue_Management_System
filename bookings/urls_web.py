from django.urls import path
from . import views_web

urlpatterns = [
    path("mine/", views_web.my_bookings_page, name="booking-mine-page"),
]