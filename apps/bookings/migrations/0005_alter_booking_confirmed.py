# Generated by Django 5.1 on 2024-08-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_confirmed_alter_booking_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
