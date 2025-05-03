from django.urls import path
from . import views
from .views import RoomListView, RoomDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', RoomListView.as_view(), name='list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='detail'),
]