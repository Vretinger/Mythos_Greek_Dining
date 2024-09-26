# bookings/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime
from django.utils import timezone

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    available = models.BooleanField(default=True)
    buffer_before = models.DurationField(default='01:00:00')  # 1 hour buffer before booking
    buffer_after = models.DurationField(default='01:00:00')   # 1 hour buffer after booking

    def __str__(self):
        return f"Table {self.table_number} - {self.capacity} seats"

# bookings/models.py

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class Booking(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_validator], max_length=17, blank=False)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField(max_length=254, blank=False)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    special_requests = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=True)  # Set default to True

    def __str__(self):
        return f"{self.guest_name} - {self.booking_date} at {self.booking_time}"

    def clean(self):
        # Call parent clean method to maintain any default validation
        super().clean()

        # Ensure booking is for a future date and time
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        booking_datetime_aware = timezone.make_aware(booking_datetime)

        # Validate that the booking date and time are not in the past
        if booking_datetime_aware < timezone.now():
            raise ValidationError('The selected date and time have already passed.')

        # Ensure number of guests doesn't exceed table capacity
        if self.table and self.number_of_guests > self.table.capacity:
            raise ValidationError(f"Number of guests exceeds the table's capacity of {self.table.capacity}.")

        # Add any other custom validation here (e.g., no conflicting bookings)

    def save(self, *args, **kwargs):
        # Call the full_clean method before saving to ensure validation
        self.full_clean()
        super().save(*args, **kwargs)

