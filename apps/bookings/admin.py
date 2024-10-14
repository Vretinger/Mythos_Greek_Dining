# bookings/admin.py

from django.contrib import admin
from .models import Table, Booking


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'available')
    list_filter = ('available',)
    search_fields = ('table_number',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'booking_date', 'booking_time',
                    'number_of_guests', 'table', 'confirmed')
    list_filter = ('booking_date', 'booking_time', 'confirmed')
    search_fields = ('guest_name',)
