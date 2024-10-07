from django.urls import path
from . import views
from .views import register, login_view, manage_bookings, custom_logout, edit_booking, delete_booking

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', register, name='signup'),  # Assuming this is your signup
    path('manage_bookings/', manage_bookings, name='manage_bookings'),
    path('logout/', custom_logout, name='logout'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]