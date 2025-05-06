from django import forms
from .models import Room, Booking, Guest

class RoomFilterForm(forms.Form):
    ROOM_TYPE_CHOICES = [('', 'Any')] + list(Room.RoomType.choices)

    room_type = forms.ChoiceField(choices=ROOM_TYPE_CHOICES, required=False, label="Room Type")
    min_capacity = forms.IntegerField(required=False, min_value=1, label="Min Capacity")
    max_capacity = forms.IntegerField(required=False, min_value=1, label="Max Capacity")
    min_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Min Price")
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label="Max Price")
    only_available = forms.BooleanField(required=False, initial=False, label="Only Available")

class BookingForm(forms.ModelForm):
    # Поля для гостя
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

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        # Перевірка: дата виїзду після дати заїзду
        if check_in_date and check_out_date and check_out_date <= check_in_date:
            raise forms.ValidationError("Check-out date must be after check-in date.")
        return cleaned_data