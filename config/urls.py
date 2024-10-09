# project_name/urls.py

from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('contact/', include('apps.contact.urls')), 
]

handler404 = 'config.views.custom_404'
handler500 = 'config.views.custom_500'
