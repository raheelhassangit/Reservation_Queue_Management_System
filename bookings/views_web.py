from django.shortcuts import render

def my_bookings_page(request):
    return render(request, "bookings/mine.html")