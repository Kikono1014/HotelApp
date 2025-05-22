from django.urls import path
from hotel.views.room import RoomListView, RoomDetailView
from .views.booking import (
    BookingCreateView, BookingListView, BookingDetailView,
    BookingCancelView, 
)
from hotel.views.home import HotelHomeView

urlpatterns = [
    path('', HotelHomeView.as_view(), name='index'),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<int:pk>/book/', BookingCreateView.as_view(), name='book_room'),

    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking_cancel'),
]
