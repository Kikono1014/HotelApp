# hotel/filters.py
import django_filters
from .models import Room

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
        field_name='is_available',
        lookup_expr='exact',
        label='Only Available'
    )

    class Meta:
        model = Room
        fields = ['room_type', 'min_capacity', 'max_capacity', 'min_price', 'max_price', 'only_available']