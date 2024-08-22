# bookings/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Automatically assign a table if not already assigned
            if not booking.table:
                available_tables = Table.objects.filter(capacity__gte=booking.number_of_guests, available=True)
                if available_tables.exists():
                    booking.table = available_tables.first()
                else:
                    messages.error(request, 'No available tables for the selected date and time.')
                    return render(request, 'bookings/booking_form.html', {'form': form})

            booking.save()
            messages.success(request, 'Your booking has been made successfully!')
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})


def booking_success(request):
    return render(request, 'bookings/booking_success.html')
