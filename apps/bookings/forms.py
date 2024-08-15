# bookings/forms.py

from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name','guest_email', 'phone', 'booking_date', 'booking_time', 'number_of_guests', 'special_requests']

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')

        # Add any additional validation here, if needed

        return cleaned_data
