# hotel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Room, Guest, Booking
from .filters import RoomFilter
from .forms import RoomFilterForm, BookingForm
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def index(request):
    context = {
        'title': 'HotelA',
        'description': 'Бронювання номерів у HotelA.'
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

    def dispatch(self, request, *args, **kwargs):
        self.room = get_object_or_404(Room, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = self.room
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.room
        context['available_periods'] = self.room.get_available_periods()
        return context

    def form_valid(self, form):
        guest, created = Guest.objects.get_or_create(
            email=form.cleaned_data['email'],
            defaults={
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data.get('phone')
            }
        )

        booking = form.save(commit=False)
        booking.room = self.room
        booking.guest = guest
        booking.status = 'confirmed'
        booking.booking_channel = 'online'
        booking.save()

        return super().form_valid(form)


class BookingListView(ListView):
    model = Booking
    template_name = 'booking/index.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.select_related('room', 'guest').order_by('-check_in_date')


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking/detail.html'
    context_object_name = 'booking'


class BookingCancelView(View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if booking.status == 'confirmed':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Бронювання успішно скасовано.')
        else:
            messages.warning(request, 'Бронювання вже скасовано або недійсне.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class GuestBookingListView(ListView):
    model = Booking
    template_name = 'booking/guest_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        email = self.request.GET.get('email')
        if email:
            qs = Booking.objects.filter(guest__email=email).select_related('room', 'guest')
            if not qs.exists():
                messages.warning(self.request, f'Бронювань для {email} не знайдено.')
            return qs
        messages.info(self.request, 'Введіть електронну адресу для пошуку ваших бронювань.')
        return Booking.objects.none()
