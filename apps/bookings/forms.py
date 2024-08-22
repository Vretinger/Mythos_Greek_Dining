# bookings/forms.py

from django import forms
from .models import Booking
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'phone', 'booking_date', 'booking_time', 'number_of_guests', 'special_requests']

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        number_of_guests = cleaned_data.get('number_of_guests')
        table = cleaned_data.get('table')

        if table:
            if number_of_guests > table.capacity:
                raise ValidationError('Number of guests exceeds the table capacity.')

            if Booking.objects.filter(table=table, booking_date=booking_date, booking_time=booking_time).exists():
                raise ValidationError('This table is already booked for the selected date and time.')

        return cleaned_data