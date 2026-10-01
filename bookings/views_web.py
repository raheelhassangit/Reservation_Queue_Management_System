from django.shortcuts import render

def my_bookings_page(request):
    return render(request, "bookings/mine.html")

def booking_confirmation_page(request, pk):
    return render(request, "bookings/confirmation.html")