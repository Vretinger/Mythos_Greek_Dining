from django.urls import path
from .views import contact_view, message_view


urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('contact/message/', message_view, name='message_view'),  # Updated URL path
]
