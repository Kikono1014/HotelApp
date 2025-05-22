from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Booking, Room, Guest
from ..forms import BookingForm

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.select_related('room', 'guest').order_by('-check_in_date')

class BookingDetailView(DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

class BookingCancelView(View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        if booking.status == 'confirmed':
            booking.status = 'canceled'
            booking.save()
            messages.success(request, 'Бронювання успішно скасовано.')
        else:
            messages.warning(request, 'Бронювання вже скасовано або недійсне.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = 'booking/book.html'
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
