from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Booking, Room, Guest
from ..forms import BookingForm
from django.views.generic.edit import FormView
from ..forms import PhoneLoginForm


class BookingLoginView(FormView):
    template_name = 'bookings/login.html'
    form_class = PhoneLoginForm

    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        return HttpResponseRedirect(f"/bookings/?phone={phone}")

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        phone = self.request.GET.get('phone')
        if phone:
            return Booking.objects.filter(guest__phone=phone).select_related('room', 'guest').order_by('-check_in_date')
        return Booking.objects.none()

class BookingDetailView(DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

class BookingCancelView(DeleteView):
    model = Booking
    template_name = 'bookings/confirm_cancel.html'  
    success_url = reverse_lazy('booking_list') 

class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = 'bookings/book.html'
    success_url = reverse_lazy('booking_list')

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
