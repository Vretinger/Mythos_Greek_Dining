from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import BookingForm
from .models import Booking, Table

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            booking_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))

            # Check if the booking datetime is in the past
            if booking_datetime < timezone.now():
                error_message = 'The selected date and time have already passed. Please choose a future date and time.'
                form.add_error(None, error_message)  # Add the error to the form
                return render(request, 'bookings/booking_form.html', {'form': form, 'error_message': error_message})

            booking = Booking(
                guest_name=form.cleaned_data['guest_name'],
                guest_email=form.cleaned_data['guest_email'],
                phone=form.cleaned_data['phone'],
                booking_date=booking_date,
                booking_time=booking_time,
                number_of_guests=form.cleaned_data['number_of_guests'],
                special_requests=form.cleaned_data['special_requests'],
                confirmed=False  # Assuming you want to set confirmed to False initially
            )

            # Automatically assign a table if one is not already selected
            if not booking.table:
                potential_tables = Table.objects.filter(
                    capacity__gte=booking.number_of_guests,
                    available=True
                )

                available_tables = []
                for table in potential_tables:
                    buffer_before = table.buffer_before
                    buffer_after = table.buffer_after

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

            # Validate and save the booking instance
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, 'Your booking has been made successfully!')
                return redirect('bookings:booking_success')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)

        else:
            messages.error(request, 'There was an error with your booking. Please correct the errors below.')
        
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})

def booking_success(request):
    return render(request, 'bookings/booking_success.html')
