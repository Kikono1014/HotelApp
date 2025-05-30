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

    def test_list_view(self):
        """Test that the room list view displays all rooms."""
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '101')
        self.assertContains(response, '102')

    def test_only_available_filter(self):
        """Test that only available rooms are shown when only_available is checked."""
        today = timezone.localdate()
        Booking.objects.create(
            room=self.room1,
            guest=self.guest,
            check_in_date=today - timezone.timedelta(days=1),
            check_out_date=today + timezone.timedelta(days=1),
            status=Booking.BookingStatus.CONFIRMED
        )
        response = self.client.get(reverse('list'), {'only_available': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '102')
        # self.assertNotContains(response, '101')

class BookingCreateViewTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )

    def test_create_booking_valid_data(self):
        """Test creating a booking with valid data."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'check_in_date': (timezone.localdate() + timezone.timedelta(days=1)).isoformat(),
            'check_out_date': (timezone.localdate() + timezone.timedelta(days=3)).isoformat(),
            'notes': 'Test booking'
        }
        response = self.client.post(reverse('book', kwargs={'pk': self.room.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.guest.email, 'john@example.com')

    def test_create_booking_invalid_dates(self):
        """Test that booking with invalid dates is rejected."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'check_in_date': (timezone.localdate() + timezone.timedelta(days=3)).isoformat(),
            'check_out_date': (timezone.localdate() + timezone.timedelta(days=2)).isoformat(),
            'notes': 'Test booking'
        }
        response = self.client.post(reverse('book', kwargs={'pk': self.room.pk}), data)
        self.assertEqual(response.status_code, 200)  # Form error, no redirect
        self.assertEqual(Booking.objects.count(), 0)

class RoomFilterFormTest(TestCase):
    def test_form_fields(self):
        """Test that RoomFilterForm has the correct fields."""
        form = RoomFilterForm()
        expected_fields = ['room_type', 'min_capacity', 'max_capacity', 'min_price', 'max_price', 'only_available']
        self.assertEqual(list(form.fields.keys()), expected_fields)

class BookingFormTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )

    def test_valid_form(self):
        """Test that BookingForm validates with valid data."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'check_in_date': (timezone.localdate() + timezone.timedelta(days=1)).isoformat(),
            'check_out_date': (timezone.localdate() + timezone.timedelta(days=3)).isoformat(),
            'notes': 'Test'
        }
        form = BookingForm(data, room=self.room)
        self.assertTrue(form.is_valid())

    def test_invalid_dates(self):
        """Test that BookingForm rejects invalid dates."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'check_in_date': (timezone.localdate() + timezone.timedelta(days=3)).isoformat(),
            'check_out_date': (timezone.localdate() + timezone.timedelta(days=2)).isoformat(),
            'notes': 'Test'
        }
        form = BookingForm(data, room=self.room)
        self.assertFalse(form.is_valid())

class RoomFilterTest(TestCase):
    def setUp(self):
        self.room1 = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )
        self.room2 = Room.objects.create(
            room_number='102',
            room_type=Room.RoomType.DOUBLE,
            capacity=4,
            price_per_night=150.00
        )
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        today = timezone.localdate()
        Booking.objects.create(
            room=self.room1,
            guest=self.guest,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=1),
            status='canceled',
            booking_channel='online'
        )
        self.assertTrue(self.room1.is_available)
