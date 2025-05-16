# hotel/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Booking, Room

@receiver(post_delete, sender=Booking)
def update_room_availability(sender, instance, **kwargs):
    room = instance.room
    active_bookings = Booking.objects.filter(
        room=room,
        status__in=['confirmed', 'checked_in']
    ).exists()
    room.is_available = not active_bookings
    room.save()