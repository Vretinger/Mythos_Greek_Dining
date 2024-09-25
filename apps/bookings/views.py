from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking, Table

def booking_create(request):
    # Check if the request is a POST (form submission)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create a booking instance but do not save it yet
            booking = form.save(commit=False)

            # Combine the booking date and time to create a datetime object
            booking_datetime = timezone.make_aware(datetime.combine(booking.booking_date, booking.booking_time))
            
            # Ensure the selected booking time is in the future
            if booking_datetime < timezone.now():
                messages.error(request, 'The selected date and time have already passed. Please choose a future date and time.')
                return render(request, 'bookings/booking_form.html', {'form': form})

            # Automatically assign a table if one is not already selected
            if not booking.table:
                # Find tables that can accommodate the number of guests and are marked as available
                potential_tables = Table.objects.filter(
                    capacity__gte=booking.number_of_guests,
                    available=True
                )

                available_tables = []
                # Check each potential table for availability, considering buffer times
                for table in potential_tables:
                    buffer_before = table.buffer_before
                    buffer_after = table.buffer_after

                    # Ensure the table is not already booked at the requested time (with buffer before/after)
                    if not Booking.objects.filter(
                        table=table,
                        booking_date=booking.booking_date,
                        booking_time__range=(
                            (booking_datetime - buffer_before).time(),
                            (booking_datetime + buffer_after).time()
                        )
                    ).exists():
                        available_tables.append(table)

                # Assign the first available table or show an error if none are available
                if available_tables:
                    booking.table = available_tables[0]
                else:
                    messages.error(request, f"No available tables for {booking.number_of_guests} people at the selected date and time.")
                    return render(request, 'bookings/booking_form.html', {'form': form})

            # Save the booking and show success message
            booking.save()
            messages.success(request, 'Your booking has been made successfully!')
            return redirect('bookings:booking_success')
        else:
            # If the form is invalid, return the form with error messages
            messages.error(request, 'There was an error with your booking. Please correct the errors below.')
            return render(request, 'bookings/booking_form.html', {'form': form})
    else:
        # If the request is GET, display a blank booking form
        form = BookingForm()

    # Render the booking form template
    return render(request, 'bookings/booking_form.html', {'form': form})


def booking_success(request):
    # Render the booking success page after the booking has been completed
    return render(request, 'bookings/booking_success.html')
