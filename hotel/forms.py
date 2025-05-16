# hotel/forms.py
from django import forms
from .models import Room, Booking, Guest
from datetime import date, timedelta

class RoomFilterForm(forms.Form):
    ROOM_TYPE_CHOICES = [('', 'Any')] + list(Room.RoomType.choices)

    room_type = forms.ChoiceField(choices=ROOM_TYPE_CHOICES, required=False, label="Room Type")
    min_capacity = forms.IntegerField(required=False, min_value=1, label="Min Capacity")
    max_capacity = forms.IntegerField(required=False, min_value=1, label="Max Capacity")
    min_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Min Price")
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Max Price")
    only_available = forms.BooleanField(required=False, initial=False, label="Only Available")

class BookingForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=20, required=False, label="Phone")

    # Нове поле для вибору періоду
    available_period = forms.ChoiceField(
        choices=[],
        required=True,
        label="Select Available Period"
    )

    class Meta:
        model = Booking
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'notes': 'Additional Notes (optional)',
        }

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        if room:
            # Заповнюємо вибір періодів
            periods = room.get_available_periods()
            choices = [
                (
                    f"{period[0]}:{period[1]}",
                    f"{period[0]} to {period[1]}"
                )
                for period in periods
            ]
            self.fields['available_period'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        available_period = cleaned_data.get('available_period')

        if available_period:
            # Розпарсуємо вибраний період
            check_in_str, check_out_str = available_period.split(':')
            check_in_date = date.fromisoformat(check_in_str)
            check_out_date = date.fromisoformat(check_out_str)

            # Перевірка: дата виїзду після дати заїзду
            if check_out_date <= check_in_date:
                raise forms.ValidationError("Check-out date must be after check-in date.")

            # Перевірка: максимум 30 днів наперед
            max_date = date.today() + timedelta(days=30)
            if check_in_date > max_date or check_out_date > max_date:
                raise forms.ValidationError("Bookings can only be made up to 30 days in advance.")

            # Перевірка: чи період дійсно вільний
            if self.room:
                conflicting_bookings = Booking.objects.filter(
                    room=self.room,
                    status__in=['confirmed', 'checked_in'],
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date
                ).exists()
                if conflicting_bookings:
                    raise forms.ValidationError("Selected period is no longer available.")

            # Додаємо очищені дати до cleaned_data
            cleaned_data['check_in_date'] = check_in_date
            cleaned_data['check_out_date'] = check_out_date

        return cleaned_data