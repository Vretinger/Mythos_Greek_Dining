from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking, Table

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            booking_date = form.cleaned_data.get('booking_date')
            booking_time = form.cleaned_data.get('booking_time')

            # Debugging output
            print(f"Booking Date: {booking_date}, Booking Time: {booking_time}")

            # Check if the booking_date or booking_time is None
            if booking_date is None or booking_time is None:
                form.add_error(None, 'Booking date and time must be provided.')
                return render(request, 'bookings/booking_form.html', {'form': form})

            booking_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))

            # Check if the booking datetime is in the past
            if booking_datetime < timezone.now():
                form.add_error(None, 'The selected date and time have already passed. Please choose a future date and time.')
                return render(request, 'bookings/booking_form.html', {'form': form})

            # Store the booking information in the session for later use
            request.session['booking_data'] = {
                'guest_name': form.cleaned_data['guest_name'],
                'guest_email': form.cleaned_data['guest_email'],
                'phone': form.cleaned_data['phone'],
                'booking_date': booking_date,
                'booking_time': booking_time,
                'num_of_guests': form.cleaned_data['number_of_guests'],
                'special_requests': form.cleaned_data['special_requests'],
            }

            # If user is authenticated, save the booking now
            if request.user.is_authenticated:
                booking = Booking(
                    guest_name=form.cleaned_data['guest_name'],
                    guest_email=form.cleaned_data['guest_email'],
                    phone=form.cleaned_data['phone'],
                    booking_date=booking_date,
                    booking_time=booking_time,
                    num_of_guests=form.cleaned_data['num_of_guests'],
                    special_requests=form.cleaned_data['special_requests'],
                    user=request.user,
                    confirmed=True,  # Mark as confirmed
                )
                booking.save()
                messages.success(request, 'Your booking has been confirmed successfully!')
                return redirect('bookings:booking_success')

            # Redirect to login/signup if user is not authenticated
            return redirect('login')  # Adjust this to your actual login URL

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form})

def booking_success(request):
    # Check if booking data exists in session
    if request.user.is_authenticated and 'booking_data' in request.session:
        booking_data = request.session['booking_data']

        # Create a booking instance
        booking = Booking(
            guest_name=booking_data['guest_name'],
            guest_email=booking_data['guest_email'],
            phone=booking_data['phone'],
            booking_date=booking_data['booking_date'],
            booking_time=booking_data['booking_time'],
            num_of_guests=booking_data['num_of_guests'],
            special_requests=booking_data['special_requests'],
            user=request.user,  # Associate booking with the logged-in user
            confirmed=True,  # Mark as confirmed
        )
        booking.save()
        messages.success(request, 'Your booking has been confirmed successfully!')

        # Clear the booking data from the session
        del request.session['booking_data']

    return render(request, 'bookings/booking_success.html')
