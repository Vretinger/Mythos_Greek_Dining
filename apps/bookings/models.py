# bookings/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from datetime import datetime, time
from django.utils import timezone

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    available = models.BooleanField(default=True)
    buffer_before = models.DurationField(default='01:00:00')  # 1 hour buffer before booking
    buffer_after = models.DurationField(default='01:00:00')   # 1 hour buffer after booking

    def __str__(self):
        return f"Table {self.table_number} - {self.capacity} seats"


class Booking(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'."
    )
    phone = models.CharField(validators=[phone_validator], max_length=17, blank=False)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField(max_length=254, blank=False)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    allergies = models.TextField(blank=True, null=True)
    dietary_preferences = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=True)  # Set default to True
    
    # Foreign key to associate booking with user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='booking_set_bookings',
        null=True   # Custom related name
    )


    
    def __str__(self):
        return f"Booking for {self.guest_name} on {self.booking_date} at {self.booking_time}"

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        # Define allowed booking time range
        opening_time = time(10, 0)  # 10:00 AM
        closing_time = time(22, 0)  # 10:00 PM

        
        # Make sure cleaned_data is not None
        if cleaned_data is None:
            cleaned_data = {}
            
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        number_of_guests = cleaned_data.get('number_of_guests')
        table = cleaned_data.get('table')


        # Validate booking time
        if not (opening_time <= self.booking_time <= closing_time):
            raise ValidationError({
                'booking_time': _('Booking time must be between 10:00 and 22:00.')
            })


        # Validate table variable presence and get its buffer times
        if table:
            buffer_before = table.buffer_before
            buffer_after = table.buffer_after

            # Combine date and time only if both are provided
            booking_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))

            # Check if the number of guests exceeds the table capacity
            if number_of_guests > table.capacity:
                raise ValidationError('Number of guests exceeds the table capacity.')

            # Check for booking conflicts
            if Booking.objects.filter(
                table=table,
                booking_date=booking_date,
                booking_time__range=(
                    (booking_datetime - buffer_before).time(),
                    (booking_datetime + buffer_after).time()
                )
            ).exists():
                raise ValidationError('This table is already booked for the selected date and time.')
        

        return cleaned_data

