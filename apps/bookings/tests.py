# bookings/tests.py

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, Table
from .forms import BookingForm


class BookingModelTest(TestCase):
    def setUp(self):
        # Create a sample table for testing
        self.table = Table.objects.create(table_number=1, capacity=4, available=True)

    def test_booking_creation(self):
        # Test if booking can be successfully created
        booking = Booking.objects.create(
            guest_name='John Doe',
            guest_email='johndoe@example.com',
            phone='+1234567890',
            booking_date=timezone.now().date() + timedelta(days=1),
            booking_time=(timezone.now() + timedelta(hours=2)).time(),
            number_of_guests=3,
            table=self.table,
        )
        self.assertEqual(str(booking), f"John Doe - {booking.booking_date} at {booking.booking_time}")

    def test_table_capacity(self):
        # Test that the table capacity is respected
        booking = Booking(
            guest_name='Jane Doe',
            guest_email='janedoe@example.com',
            phone='+1234567891',
            booking_date=timezone.now().date() + timedelta(days=1),
            booking_time=(timezone.now() + timedelta(hours=2)).time(),
            number_of_guests=10,  # exceeds capacity
            table=self.table,
        )
        with self.assertRaises(ValidationError):
            booking.save()


class BookingFormTest(TestCase):
    def setUp(self):
        # Set up the necessary table for form tests
        self.table = Table.objects.create(table_number=1, capacity=4, available=True)

    def test_valid_booking_form(self):
        # Test if a valid form submission is accepted
        form_data = {
            'guest_name': 'John Doe',
            'guest_email': 'johndoe@example.com',
            'phone': '+1234567890',
            'booking_date': timezone.now().date() + timedelta(days=1),
            'booking_time': (timezone.now() + timedelta(hours=2)).time(),
            'number_of_guests': 3,
            'special_requests': 'Vegetarian meal',
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        # Test invalid email
        form_data = {
            'guest_name': 'John Doe',
            'guest_email': 'not-an-email',
            'phone': '+1234567890',
            'booking_date': timezone.now().date() + timedelta(days=1),
            'booking_time': (timezone.now() + timedelta(hours=2)).time(),
            'number_of_guests': 3,
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('guest_email', form.errors)


class BookingViewTest(TestCase):
    def setUp(self):
        # Set up sample table for views
        self.table = Table.objects.create(table_number=1, capacity=4, available=True)

    def test_booking_create_view(self):
        # Test GET request to the booking create view
        response = self.client.get(reverse('bookings:booking_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_form.html')

    def test_successful_booking_submission(self):
        # Test POST request with valid data
        form_data = {
            'guest_name': 'John Doe',
            'guest_email': 'johndoe@example.com',
            'phone': '+1234567890',
            'booking_date': timezone.now().date() + timedelta(days=1),
            'booking_time': (timezone.now() + timedelta(hours=2)).time(),
            'number_of_guests': 3,
        }
        response = self.client.post(reverse('bookings:booking_create'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to success page
        self.assertRedirects(response, reverse('bookings:booking_success'))

    def test_booking_submission_past_date(self):
        # Set up a past booking date
        past_date = timezone.now().date() - timedelta(days=1)
        future_time = (timezone.now() + timedelta(hours=2)).time()

        # Post the booking data to the view
        response = self.client.post('/bookings/book/', {
            'guest_name': 'Jane Doe',
            'guest_email': 'janedoe@example.com',
            'phone': '+1234567891',
            'booking_date': past_date,
            'booking_time': future_time,
            'number_of_guests': 3,
            'special_requests': 'None',
        })

        # Assert that the response contains the validation error message
        self.assertContains(response, 'The selected date and time have already passed.')
