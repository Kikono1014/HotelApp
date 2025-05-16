# hotel/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Room, Guest, Booking
from .filters import RoomFilter
from .forms import RoomFilterForm, BookingForm

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
        context['filterset'] = self.filterset
        return context

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/detail.html'
    context_object_name = 'room'

class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = 'book.html'
    success_url = reverse_lazy('list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = Room.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = Room.objects.get(pk=self.kwargs['pk'])
        context['room'] = room
        context['available_periods'] = room.get_available_periods()
        return context

    def form_valid(self, form):
        room = Room.objects.get(pk=self.kwargs['pk'])
        guest, created = Guest.objects.get_or_create(
            email=form.cleaned_data['email'],
            defaults={
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'] or None
            }
        )

        booking = form.save(commit=False)
        booking.room = room
        booking.guest = guest
        booking.status = 'confirmed'
        booking.booking_channel = 'online'
        booking.save()

        room.save()

        return super().form_valid(form)