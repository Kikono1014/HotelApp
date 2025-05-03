# your_app/forms.py
from django import forms
from .models import Room

class RoomFilterForm(forms.Form):
    ROOM_TYPE_CHOICES = [('', 'Any')] + list(Room.RoomType.choices)

    room_type = forms.ChoiceField(choices=ROOM_TYPE_CHOICES, required=False, label="Room Type")
    min_capacity = forms.IntegerField(required=False, min_value=1, label="Min Capacity")
    max_capacity = forms.IntegerField(required=False, min_value=1, label="Max Capacity")
    min_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Min Price")
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Max Price")
    is_available = forms.BooleanField(required=False, initial=False, label="Only Available")
