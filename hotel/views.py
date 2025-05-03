from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Room
from .filters import RoomFilter
from .forms import RoomFilterForm

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

    filterset_class = RoomFilter

   
    def get_queryset(self):
        qs = super().get_queryset()

        data = self.request.GET.copy()

        self.filterset = self.filterset_class(data, queryset=qs)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = RoomFilterForm(self.request.GET)
        context['filterset']   = self.filterset
        return context

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/detail.html'
    context_object_name = 'room'