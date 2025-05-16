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

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'notes']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'check_in_date': 'Check-in Date',
            'check_out_date': 'Check-out Date',
            'notes': 'Additional Notes (optional)',
        }

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        if room:
            # Set min and max dates based on available periods
            today = date.today()
            max_date = today + timedelta(days=30)
            periods = room.get_available_periods()
            if periods:
                # Use the earliest available date as the minimum
                min_date = periods[0][0]
                self.fields['check_in_date'].widget.attrs.update({
                    'min': min_date.isoformat(),
                    'max': max_date.isoformat()
                })
                self.fields['check_out_date'].widget.attrs.update({
                    'min': (min_date + timedelta(days=1)).isoformat(),
                    'max': max_date.isoformat()
                })

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date:
            # Check if check-out is after check-in
            if check_out_date <= check_in_date:
                raise forms.ValidationError("Check-out date must be after check-in date.")

            # Check if dates are within 30 days
            max_date = date.today() + timedelta(days=30)
            if check_in_date > max_date or check_out_date > max_date:
                raise forms.ValidationError("Bookings can only be made up to 30 days in advance.")

            # Check if the selected range falls within an available period
            if self.room:
                periods = self.room.get_available_periods()
                is_valid_period = False
                for period in periods:
                    period_start, period_end = period
                    if (check_in_date >= period_start and check_out_date <= period_end):
                        is_valid_period = True
                        break
                if not is_valid_period:
                    raise forms.ValidationError("Selected dates are not within an available period.")

                # Check for overlapping bookings
                conflicting_bookings = Booking.objects.filter(
                    room=self.room,
                    status__in=['confirmed', 'checked_in'],
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date
                ).exists()
                if conflicting_bookings:
                    raise forms.ValidationError("Room is not available for the selected dates.")

        return cleaned_data