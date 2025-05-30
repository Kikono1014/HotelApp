from django.test import TestCase
from datetime import date, timedelta
from .models import Room, Booking, Guest

class RoomModelTest(TestCase):
    def setUp(self):
        self.guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890"
        )

        self.room1 = Room.objects.create(
            room_number='101',
            room_type='single',
            price_per_night=100.00,
            capacity=1
        )
        self.room2 = Room.objects.create(
            room_number='102',
            room_type='double',
            price_per_night=150.00,
            capacity=2
        )

    def test_is_available_no_bookings(self):
        self.assertTrue(self.room2.is_available)

    def test_is_available_with_confirmed_booking(self):
        Booking.objects.create(
            room=self.room1,
            guest=self.guest,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=1),
            status='confirmed',
            booking_channel='online'
        )
        self.assertFalse(self.room1.is_available)

    def test_is_available_with_canceled_booking(self):
        Booking.objects.create(
            room=self.room1,
            guest=self.guest,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=1),
            status='canceled',
            booking_channel='online'
        )
        self.assertTrue(self.room1.is_available)
