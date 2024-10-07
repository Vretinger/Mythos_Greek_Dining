from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .forms import BookingForm, CustomUserCreationForm, CustomAuthenticationForm
from apps.bookings.models import Booking


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Automatically log the user in
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(request, email=email, password=raw_password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f"Account created for {email}!")
                return redirect('manage_bookings')  # Redirect to some page after login
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('manage_bookings') 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('home')

def manage_bookings(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)

        # Update the `confirmed` status for bookings that have passed
        for booking in bookings:
            booking_datetime = timezone.make_aware(
                datetime.combine(booking.booking_date, booking.booking_time)
            )
            if booking_datetime < timezone.now() and booking.confirmed:
                booking.confirmed = False
                booking.save()
    else:
        bookings = Booking.objects.none()

    return render(request, 'manage_bookings.html', {'bookings': bookings})


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('manage_bookings')  # Adjust this as needed
    else:
        form = BookingForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        return redirect('manage_bookings')  # Redirect to the bookings management page

    return render(request, 'manage_bookings', {'booking': booking})



def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if request.user.is_authenticated:
                booking.user = request.user
                booking.guest_email = request.user.email  # Ensure guest_email is set
                booking.save()
                return redirect('manage_bookings')
            else:
                # Store booking data in session for unauthenticated users
                request.session['booking_data'] = request.POST
                return redirect('register')

    else:
        form = BookingForm()

    return render(request, 'create_booking.html', {'form': form})

