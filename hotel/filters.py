# hotel/filters.py
import django_filters
from .models import Room, Booking
from django.utils import timezone

class RoomFilter(django_filters.FilterSet):
    room_type = django_filters.ChoiceFilter(
        choices=Room.RoomType.choices,
        empty_label='Any',
        label='Room Type'
    )
    min_capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte',
        label='Min Capacity'
    )
    max_capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='lte',
        label='Max Capacity'
    )
    min_price = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='gte',
        label='Min Price'
    )
    max_price = django_filters.NumberFilter(
        field_name='price_per_night',
        lookup_expr='lte',
        label='Max Price'
    )
    
    only_available = django_filters.BooleanFilter(
        method='filter_only_available',
        label='Only Available'
    )

    class Meta:
        model = Room
        fields = ['room_type', 'min_capacity', 'max_capacity', 'min_price', 'max_price', 'only_available']

    
    def filter_only_available(self, queryset, name, value):
        print(value)
        if value:
            today = timezone.localdate()
            qs = queryset.exclude(
                booking__status__in=[Booking.BookingStatus.CONFIRMED, Booking.BookingStatus.CHECKED_IN],
                booking__check_in_date__lte=today,
                booking__check_out_date__gte=today
            )
            return qs
        return queryset