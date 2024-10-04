from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings 
from django.core.exceptions import ValidationError

class Booking(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    phone = models.CharField(max_length=15)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    num_of_guests = models.IntegerField()
    special_requests = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)

    # Foreign key to associate booking with user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='booking_set_user',
        null=True   # Custom related name
    )

    def __str__(self):
        return f'{self.guest_name} - {self.booking_date}'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)  # Make this required
    last_name = models.CharField(max_length=30, blank=False)   # Make this required
    phone_number = models.CharField(max_length=15, blank=False)  # Phone number is required
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    

    def __str__(self):
        return self.email

    def clean(self):
        # Custom validation for the model
        if self.phone_number and len(self.phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 digits.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
