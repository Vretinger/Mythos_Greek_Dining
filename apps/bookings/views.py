from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking, Table

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Debug statement: Print the form data being processed
            print(f"Form data: {form.cleaned_data}")

            # Automatically assign a table if not already assigned
            if not booking.table:
                potential_tables = Table.objects.filter(capacity__gte=booking.number_of_guests, available=True)
                print(f"Potential tables for {booking.number_of_guests} guests: {[table.table_number for table in potential_tables]}")  # Debug statement

                available_tables = []

                # Check each potential table for conflicts
                for table in potential_tables:
                    conflicting_bookings = Booking.objects.filter(
                        table=table,
                        booking_date=booking.booking_date,
                        booking_time=booking.booking_time
                    )

                    # Debug information for each table checked
                    if conflicting_bookings.exists():
                        print(f"Table {table.table_number} is not available due to conflicting bookings.")  # Debug statement
                    else:
                        print(f"Table {table.table_number} is available.")  # Debug statement
                        available_tables.append(table)

                if available_tables:
                    booking.table = available_tables[0]
                    print(f"Assigned table {booking.table.table_number} to the booking.")  # Debug statement
                else:
                    # Error message and debug output if no tables are available
                    print("No tables available for the selected date and time.")  # Debug statement
                    messages.error(request, 'Selected table is already booked for this date and time.')
                    return render(request, 'bookings/booking_form.html', {'form': form})

            booking.save()
            print(f"Booking saved: {booking}")  # Debug statement
            messages.success(request, 'Your booking has been made successfully!')
            return redirect('bookings:booking_success')
        else:
            # Debug statement: Print form errors
            print("Form is not valid")  # Debug statement
            print(form.errors)  # Debug statement
            messages.error(request, 'There was an error with your booking. Please correct the errors below.')
            return render(request, 'bookings/booking_form.html', {'form': form})
    else:
        form = BookingForm()

    # Render the booking form for GET requests
    return render(request, 'bookings/booking_form.html', {'form': form})



def booking_success(request):
    # Render a success page after booking is completed
    return render(request, 'bookings/booking_success.html')