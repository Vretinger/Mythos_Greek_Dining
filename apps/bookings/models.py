# bookings/models.py

from django.db import models

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} - {self.capacity} seats"

class Booking(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField(default='no-reply@example.com')
    phone = models.CharField(max_length=20, default='000-000-0000')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.IntegerField()
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.guest_name} - {self.booking_date} at {self.booking_time}"
