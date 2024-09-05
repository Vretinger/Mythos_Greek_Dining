from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking, Table

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Combine booking date and time
            booking_datetime = timezone.make_aware(datetime.combine(booking.booking_date, booking.booking_time))
            
            # Check if the booking date and time is in the past
            if booking_datetime < timezone.now():
                messages.error(request, 'The selected date and time have already passed. Please choose a future date and time.')
                return render(request, 'bookings/booking_form.html', {'form': form})

            # Automatically assign a table if not already assigned
            if not booking.table:
                potential_tables = Table.objects.filter(
                    capacity__gte=booking.number_of_guests,
                    available=True
                )

                available_tables = []
                for table in potential_tables:
                    buffer_before = table.buffer_before
                    buffer_after = table.buffer_after

                    # Check for availability with buffer times
                    if not Booking.objects.filter(
                        table=table,
                        booking_date=booking.booking_date,
                        booking_time__range=(
                            (booking_datetime - buffer_before).time(),
                            (booking_datetime + buffer_after).time()
                        )
                    ).exists():
                        available_tables.append(table)
                
                if available_tables:
                    booking.table = available_tables[0]
                else:
                    messages.error(request, f"No available tables for {booking.number_of_guests} people at the selected date and time.")
                    return render(request, 'bookings/booking_form.html', {'form': form})

            booking.save()
            print(f"Booking saved: {booking}")  # Debug statement
            messages.success(request, 'Your booking has been made successfully!')
            return redirect('bookings:booking_success')
        else:
            # Debug statement: Print form errors
            print("Form is not valid")  # Debug statement
            print(form.errors)  # Debug statement
            messages.error(request, 'There was an error with your booking. Please correct the errors below.')
            return render(request, 'bookings/booking_form.html', {'form': form})
    else:
        form = BookingForm()

    # Render the booking form for GET requests
    return render(request, 'bookings/booking_form.html', {'form': form})



def booking_success(request):
    # Render a success page after booking is completed
    return render(request, 'bookings/booking_success.html')