import django_filters
from .models import Room

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
    is_available  = django_filters.BooleanFilter(
                        field_name='is_available',
                        widget=django_filters.widgets.BooleanWidget(),
                        label="Only Available"
                    )

    class Meta:
        model = Room
        fields = []
