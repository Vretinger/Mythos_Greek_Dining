from django import forms
from .models import Booking, Table
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'booking_date', 'booking_time', 'number_of_guests']

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        number_of_guests = cleaned_data.get('number_of_guests')

        # Find tables that can accommodate the guest count
        potential_tables = Table.objects.filter(capacity__gte=number_of_guests, available=True)
        print(f"Potential tables for {number_of_guests} guests: {[table.table_number for table in potential_tables]}")  # Debug statement

        available_tables = []

        # Check each potential table for conflicting bookings
        for table in potential_tables:
            conflicting_bookings = Booking.objects.filter(
                table=table,
                booking_date=booking_date,
                booking_time=booking_time
            )

            if conflicting_bookings.exists():
                print(f"Table {table.table_number} is not available due to conflicting bookings.")  # Debug statement
            else:
                print(f"Table {table.table_number} is available.")  # Debug statement
                available_tables.append(table)

        # If no tables are available, raise a validation error
        if not available_tables:
            raise forms.ValidationError('Selected table is already booked for this date and time.')

        # Assign the first available table to the booking instance (you can customize this if needed)
        cleaned_data['table'] = available_tables[0] if available_tables else None

        return cleaned_data
