from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import BookingForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Booking


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_bookings')  
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


@login_required
def manage_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'manage_bookings.html', {'bookings': bookings})

def create_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()
                return redirect('manage_bookings')
        else:
            request.session['booking_data'] = request.POST
            return redirect('register')
    else:
        form = BookingForm()
    return render(request, 'create_booking.html', {'form': form})
