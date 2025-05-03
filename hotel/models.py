from django.db import models

class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = 'single', 'Single'
        DOUBLE = 'double', 'Double'
        SUITE = 'suite', 'Suite'
        FAMILY = 'family', 'Family'
        DELUXE = 'deluxe', 'Deluxe'
    
    # Показне ім’я номера
    room_number = models.CharField(max_length=10, unique=True)
    # Тип кімнати
    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        default=RoomType.SINGLE,
    )
    # Максимальна кількість гостей
    capacity = models.PositiveSmallIntegerField()
    # Ціна за ніч
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    # Опис чи особливості
    description = models.TextField(blank=True, null=True)
    # Доступність для бронювання
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

    class Meta:
        ordering = ['room_number']


class Guest(models.Model):
    # Ім’я гостя
    first_name = models.CharField(max_length=50)
    # Прізвище
    last_name = models.CharField(max_length=50)
    # Email
    email = models.EmailField(unique=True)
    # Телефон
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

    # Номер, що бронюється :contentReference[oaicite:0]{index=0}
    room = models.ForeignKey(Room,  on_delete=models.CASCADE)
    # Гість, що робить бронювання :contentReference[oaicite:1]{index=1}
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    # Дата заїзду
    check_in_date = models.DateField()
    # Дата виїзду
    check_out_date = models.DateField()
    # Коли створено бронювання
    booking_date = models.DateTimeField(auto_now_add=True)
    # Статус 
    status          = models.CharField(
        max_length=12,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )
    # Спосіб бронювання
    booking_channel = models.CharField(
        max_length=10,
        choices=BookingChannel.choices,
        default=BookingChannel.ONLINE,
    )
    # Додаткова інформація
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking {self.id}: {self.room} for {self.guest}"

    class Meta:
        ordering = ['-booking_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
