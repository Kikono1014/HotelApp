from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.db.utils import IntegrityError
from .models import Room, Guest, Booking
from .forms import RoomFilterForm, BookingForm
from .filters import RoomFilter

class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )

    def test_room_creation(self):
        """Test that a room can be created with valid data."""
        self.assertEqual(self.room.room_number, '101')
        self.assertEqual(self.room.room_type, Room.RoomType.SINGLE)
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.price_per_night, 100.00)

    def test_is_available_no_bookings(self):
        """Test that a room with no bookings is available."""
        self.assertTrue(self.room.is_available)

    def test_is_available_with_confirmed_booking(self):
        """Test that a room with a confirmed booking for today is not available."""
        today = timezone.localdate()
        Booking.objects.create(
            room=self.room,
            guest=self.guest,
            check_in_date=today - timezone.timedelta(days=1),
            check_out_date=today + timezone.timedelta(days=1),
            status=Booking.BookingStatus.CONFIRMED
        )
        self.assertFalse(self.room.is_available)

    def test_is_available_with_canceled_booking(self):
        """Test that a room with a canceled booking is available."""
        today = timezone.localdate()
        Booking.objects.create(
            room=self.room,
            guest=self.guest,
            check_in_date=today - timezone.timedelta(days=1),
            check_out_date=today + timezone.timedelta(days=1),
            status=Booking.BookingStatus.CANCELED
        )
        self.assertTrue(self.room.is_available)

    def test_get_next_available_date_no_bookings(self):
        """Test that a room with no bookings is available today."""
        self.assertEqual(self.room.get_next_available_date(), timezone.localdate())

class GuestModelTest(TestCase):
    def test_guest_creation(self):
        """Test that a guest can be created with valid data."""
        guest = Guest.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )
        self.assertEqual(guest.first_name, 'Jane')
        self.assertEqual(guest.last_name, 'Smith')
        self.assertEqual(guest.email, 'jane@example.com')

    def test_email_unique(self):
        """Test that email must be unique."""
        Guest.objects.create(email='test@example.com')
        with self.assertRaises(IntegrityError):
            Guest.objects.create(email='test@example.com')

class BookingModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )

    def test_booking_creation(self):
        """Test that a booking can be created with valid data."""
        today = timezone.localdate()
        booking = Booking.objects.create(
            room=self.room,
            guest=self.guest,
            check_in_date=today,
            check_out_date=today + timezone.timedelta(days=2),
            status=Booking.BookingStatus.CONFIRMED,
            booking_channel=Booking.BookingChannel.ONLINE
        )
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.guest, self.guest)
        self.assertEqual(booking.check_in_date, today)
        self.assertEqual(booking.check_out_date, today + timezone.timedelta(days=2))
        self.assertEqual(booking.status, Booking.BookingStatus.CONFIRMED)

class RoomListViewTest(TestCase):
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

    # def test_list_view(self):
    #     """Test that the room list view displays all rooms."""
    #     response = self.client.get(reverse('list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, '101')
    #     self.assertContains(response, '102')

    # def test_only_available_filter(self):
    #     """Test that only available rooms are shown when only_available is checked."""
    #     today = timezone.localdate()
    #     Booking.objects.create(
    #         room=self.room1,
    #         guest=self.guest,
    #         check_in_date=today - timezone.timedelta(days=1),
    #         check_out_date=today + timezone.timedelta(days=1),
    #         status=Booking.BookingStatus.CONFIRMED
    #     )
    #     response = self.client.get(reverse('list'), {'only_available': 'on'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, '102')

class BookingCreateViewTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )

    # def test_create_booking_valid_data(self):
    #     """Test creating a booking with valid data."""
    #     data = {
    #         'first_name': 'John',
    #         'last_name': 'Doe',
    #         'email': 'john@example.com',
    #         'phone': '1234567890',
    #         'check_in_date': (timezone.localdate() + timezone.timedelta(days=1)).isoformat(),
    #         'check_out_date': (timezone.localdate() + timezone.timedelta(days=3)).isoformat(),
    #         'notes': 'Test booking'
    #     }
    #     response = self.client.post(reverse('book', kwargs={'pk': self.room.pk}), data)
    #     self.assertEqual(response.status_code, 302)  # Redirect on success
    #     self.assertEqual(Booking.objects.count(), 1)
    #     booking = Booking.objects.first()
    #     self.assertEqual(booking.guest.email, 'john@example.com')

    # def test_create_booking_invalid_dates(self):
    #     """Test that booking with invalid dates is rejected."""
    #     data = {
    #         'first_name': 'John',
    #         'last_name': 'Doe',
    #         'email': 'john@example.com',
    #         'phone': '1234567890',
    #         'check_in_date': (timezone.localdate() + timezone.timedelta(days=3)).isoformat(),
    #         'check_out_date': (timezone.localdate() + timezone.timedelta(days=2)).isoformat(),
    #         'notes': 'Test booking'
    #     }
    #     response = self.client.post(reverse('book', kwargs={'pk': self.room.pk}), data)
    #     self.assertEqual(response.status_code, 200)  # Form error, no redirect
    #     self.assertEqual(Booking.objects.count(), 0)

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
            check_in_date=today - timezone.timedelta(days=1),
            check_out_date=today + timezone.timedelta(days=1),
            status=Booking.BookingStatus.CONFIRMED
        )

    def test_only_available_filter(self):
        """Test that only available rooms are shown when only_available is True."""
        filterset = RoomFilter({'only_available': 'true'}, queryset=Room.objects.all())
        self.assertEqual(filterset.qs.count(), 1)  # Only room2 should be available
        self.assertIn(self.room2, filterset.qs)
        self.assertNotIn(self.room1, filterset.qs)

    def test_no_filter(self):
        """Test that all rooms are shown when no filters are applied."""
        filterset = RoomFilter({}, queryset=Room.objects.all())
        self.assertEqual(filterset.qs.count(), 2)
        self.assertIn(self.room1, filterset.qs)
        self.assertIn(self.room2, filterset.qs)

class SignalTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            room_type=Room.RoomType.SINGLE,
            capacity=2,
            price_per_night=100.00
        )
        self.guest = Guest.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        today = timezone.localdate()
        self.booking = Booking.objects.create(
            room=self.room,
            guest=self.guest,
            check_in_date=today - timezone.timedelta(days=1),
            check_out_date=today + timezone.timedelta(days=1),
            status=Booking.BookingStatus.CONFIRMED
        )
        self.room.refresh_from_db()

    def test_update_availability_on_booking_delete(self):
        """Test that deleting a booking updates room availability."""
        self.assertFalse(self.room.is_available)
        self.booking.delete()
        self.room.refresh_from_db()
        self.assertTrue(self.room.is_available)