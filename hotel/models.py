# hotel/models.py
from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from django.utils import timezone

class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = 'single', 'Single'
        DOUBLE = 'double', 'Double'
        SUITE = 'suite', 'Suite'
        FAMILY = 'family', 'Family'
        DELUXE = 'deluxe', 'Deluxe'
    
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        default=RoomType.SINGLE,
    )
    capacity = models.PositiveSmallIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    # is_available = models.BooleanField(default=True)

    @property
    def is_available(self):
        today = timezone.localdate()
        return not Booking.objects.filter(
            room=self,
            status__in=[Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.CHECKED_IN],
            check_in_date__lte=today,
            check_out_date__gte=today,
        ).exists()
    

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

    def get_next_available_date(self):
        today = date.today()
        bookings = Booking.objects.filter(
            room=self,
            status__in=['confirmed', 'checked_in'],
            check_out_date__gte=today
        ).order_by('check_out_date')
        
        if not bookings.exists():
            return today
        
        last_booking = bookings.last()
        return last_booking.check_out_date

    def get_available_periods(self, max_days=30):
        today = date.today()
        max_date = today + timedelta(days=max_days)
        bookings = Booking.objects.filter(
            room=self,
            status__in=['confirmed', 'checked_in'],
            check_out_date__gte=today,
            check_in_date__lte=max_date
        ).order_by('check_in_date')

        periods = []
        current_date = today

        if not bookings.exists():
            return [(today, max_date)]

        for booking in bookings:
            if current_date < booking.check_in_date:
                periods.append((current_date, booking.check_in_date))
            current_date = max(current_date, booking.check_out_date)

        if current_date < max_date:
            periods.append((current_date, max_date))

        return periods

    class Meta:
        ordering = ['room_number']

class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']

class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        CONFIRMED   = 'confirmed', 'Confirmed'
        CANCELED    = 'canceled', 'Canceled'
        CHECKED_IN  = 'checked_in', 'Checked In'
        CHECKED_OUT = 'checked_out', 'Checked Out'

    class BookingChannel(models.TextChoices):
        ONLINE     = 'online', 'Online'
        PHONE      = 'phone', 'Phone'
        IN_PERSON  = 'in_person', 'In Person'
        AGENT      = 'agent', 'Travel Agent'

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=12,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )
    booking_channel = models.CharField(
        max_length=10,
        choices=BookingChannel.choices,
        default=BookingChannel.ONLINE,
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking {self.id}: {self.room} for {self.guest}"

    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'