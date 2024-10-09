from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .encoders import DateJSONEncoder 
from .forms import BookingForm
from .models import Booking

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data.get('booking_date')
            booking_time = form.cleaned_data.get('booking_time')

            if booking_date is None or booking_time is None:
                form.add_error(None, 'Booking date and time must be provided.')
                return render(request, 'bookings/booking_form.html', {'form': form})

            booking_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))
            if booking_datetime < timezone.now():
                form.add_error(None, 'The selected date and time have already passed. Please choose a future date and time.')
                return render(request, 'bookings/booking_form.html', {'form': form})

            # Store booking info in session for later use if not authenticated
            request.session['booking_data'] = {
                'guest_name': form.cleaned_data['guest_name'],
                'guest_email': form.cleaned_data['guest_email'],
                'phone': form.cleaned_data['phone'],
                'booking_date': booking_date.strftime('%Y-%m-%d'),  # Convert to string
                'booking_time': booking_time.strftime('%H:%M'),  # Convert to string
                'number_of_guests': form.cleaned_data['number_of_guests'],
                'allergies': form.cleaned_data.get('allergies'),  # Optional field
                'dietary_preferences': form.cleaned_data.get('dietary_preferences'),  # Optional field
                'additional_notes': form.cleaned_data.get('additional_notes'),  # Optional field
            }

            if request.user.is_authenticated:
                # Save booking immediately for authenticated users
                booking = form.save(commit=False)
                booking.user = request.user
                booking.guest_email = request.user.email  # Ensure email is saved
                booking.save()
                messages.success(request, 'Your booking has been confirmed successfully!')
                del request.session['booking_data']  # Clear session after booking
                return redirect('bookings:booking_success')

            # Redirect to login/signup if user is not authenticated
            messages.info(request, 'Please log in or sign up to confirm your booking.')
            return redirect(f"{reverse('login')}?next={request.path}")  # Redirect to login/signup

    else:
        # Check if there is booking data in the session (after login/signup)
        session_booking_data = request.session.get('booking_data', None)
        form_data = session_booking_data if session_booking_data else {}

        # If user is logged in, prepopulate form with user details
        if request.user.is_authenticated:
            form_data.update({
                'guest_name': request.user.get_full_name() or request.user.username,
                'guest_email': request.user.email,
                'phone': request.user.phone_number,  
            })

        # Initialize the form with either session or user data
        form = BookingForm(initial=form_data)

    return render(request, 'bookings/booking_form.html', {'form': form})




def booking_success(request):
    # Check if booking data exists in session
    if request.user.is_authenticated and 'booking_data' in request.session:
        booking_data = request.session['booking_data']

        # Create a booking instance
        booking = Booking.objects.create(
            guest_name=booking_data['guest_name'],
            guest_email=request.user.email,
            phone=booking_data['phone'],
            booking_date=booking_data['booking_date'],
            booking_time=booking_data['booking_time'],
            number_of_guests=booking_data['number_of_guests'],
            allergies=booking_data['allergies'],
            dietary_preferences=booking_data['dietary_preferences'],
            additional_notes=booking_data['additional_notes'],
            user=request.user,  # Associate booking with the logged-in user
            confirmed=True,  # Mark as confirmed
        )
        booking.save()
        messages.success(request, 'Your booking has been confirmed successfully!')

        # Clear the booking data from the session
        del request.session['booking_data']

        # Return a JSON response (optional)
        return JsonResponse({
            'message': 'Your booking has been confirmed successfully!',
            'booking_data': {
                'guest_name': booking.guest_name,
                'guest_email': booking.guest_email,
                'booking_date': booking.booking_date,
                'booking_time': booking.booking_time,
            }
        }, encoder=DateJSONEncoder)

    return render(request, 'bookings/booking_success.html')

