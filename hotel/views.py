from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Room

def index(request):
    context = {
        'title': 'HotelA',
        'description': 'Booking rooms in HotelA.'
    }
    return render(request, 'index.html', context)


class RoomListView(ListView):
    model = Room
    template_name = 'rooms/index.html'
    context_object_name = 'rooms'
    paginate_by = 10

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/detail.html'
    context_object_name = 'room'