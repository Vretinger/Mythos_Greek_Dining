from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Booking
import re



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'phone', 'booking_date', 'booking_time', 'num_of_guests', 'special_requests']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)
