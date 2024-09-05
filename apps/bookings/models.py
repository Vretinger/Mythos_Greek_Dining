# bookings/models.py

from django.db import models
from django.core.validators import RegexValidator

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    available = models.BooleanField(default=True)
    buffer_before = models.DurationField(default='01:00:00')  # 1 hour buffer before booking
    buffer_after = models.DurationField(default='01:00:00')   # 1 hour buffer after booking

    def __str__(self):
        return f"Table {self.table_number} - {self.capacity} seats"

# bookings/models.py

class Booking(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_validator], max_length=17, blank=True)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField(default='no-reply@example.com')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    special_requests = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=True)  # Set default to True

    def __str__(self):
        return f"{self.guest_name} - {self.booking_date} at {self.booking_time}"

