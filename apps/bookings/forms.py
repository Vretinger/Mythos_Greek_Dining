# bookings/forms.py

from django import forms
from .models import Booking, Table
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'phone', 'booking_date', 'booking_time', 'number_of_guests', 'special_requests']
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'Book Now'))
        self.helper.layout = Layout(
            Row(
                Column(Field('guest_name', css_class='form-control'), css_class='form-group col-md-6 mb-0'),
                Column(Field('guest_email', css_class='form-control'), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field('phone', css_class='form-control'), css_class='form-group col-md-6 mb-0'),
                Column(Field('booking_date', css_class='form-control'), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field('booking_time', css_class='form-control'), css_class='form-group col-md-6 mb-0'),
                Column(Field('number_of_guests', css_class='form-control'), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('special_requests', css_class='form-control'),
        )

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        number_of_guests = cleaned_data.get('number_of_guests')
        table = cleaned_data.get('table')

        if table:
            buffer_before = table.buffer_before
            buffer_after = table.buffer_after
            booking_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))

            if number_of_guests > table.capacity:
                raise ValidationError('Number of guests exceeds the table capacity.')

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
