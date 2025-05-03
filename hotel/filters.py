import django_filters
from .models import Room
from django import forms

class RoomFilter(django_filters.FilterSet):
    room_type     = django_filters.ChoiceFilter(
                        choices=Room.RoomType.choices,
                        label="Room Type",
                        empty_label="Any",
                    )
    min_capacity  = django_filters.NumberFilter(
                        field_name='capacity', lookup_expr='gte',
                        label="Min Capacity"
                    )
    max_capacity  = django_filters.NumberFilter(
                        field_name='capacity', lookup_expr='lte',
                        label="Max Capacity"
                    )
    min_price     = django_filters.NumberFilter(
                        field_name='price_per_night', lookup_expr='gte',
                        label="Min Price"
                    )
    max_price     = django_filters.NumberFilter(
                        field_name='price_per_night', lookup_expr='lte',
                        label="Max Price"
                    )
    only_available = django_filters.BooleanFilter(
                        field_name='is_available',
                        widget=forms.CheckboxInput,
                        label="Only Available",
                        method='filter_by_availability'
                    )

    class Meta:
        model = Room
        fields = []

    
    def filter_by_availability(self, queryset, name, value):
        """
        If the checkbox is checked (value=True), return only available rooms.
        If unchecked (value=False or None), return all rooms.
        """
        if value:
            return queryset.filter(is_available=True)
        return queryset  # unchecked → no filtering
