# apps/bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.booking_create, name='booking_create'),
    path('success/', views.booking_success, name='booking_success'),
]
