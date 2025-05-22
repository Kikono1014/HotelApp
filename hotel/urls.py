from django.urls import path
from . import views
from .views import (
    index,
    RoomListView,
    RoomDetailView,
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    BookingCancelView,
    GuestBookingListView,
)

urlpatterns = [
    path('', index, name='index'),
    path('rooms/', RoomListView.as_view(), name='list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='detail'),
    path('rooms/<int:pk>/book/', BookingCreateView.as_view(), name='book'),

    # Новые маршруты для бронирований
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking_cancel'),
    path('my-bookings/', GuestBookingListView.as_view(), name='guest_booking_list'),
]
