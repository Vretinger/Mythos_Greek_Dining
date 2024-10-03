from django.urls import path
from .views import register, login_view, manage_bookings

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', register, name='signup'),  # Assuming this is your signup
    path('manage_bookings/', manage_bookings, name='manage_bookings'),
]