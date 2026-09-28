# bookings/admin.py
from django.contrib import admin
from .models import Booking, BookingSeat

admin.site.register(Booking)
admin.site.register(BookingSeat)