from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from ..models import Room
from ..filters import RoomFilter
from ..forms import RoomFilterForm

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        data = self.request.GET.copy()
        self.filterset = RoomFilter(data, queryset=qs)

        if self.request.GET.get('available') == 'true':
            return [room for room in self.filterset.qs if room.is_available]

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = RoomFilterForm(self.request.GET)
        context['filterset'] = self.filterset
        return context

class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

@staff_member_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = RoomForm()
    return render(request, 'rooms/add_edit.html', {'form': form})

@staff_member_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('detail', pk=room.id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/add_edit.html', {'form': form, 'edit': True})

@staff_member_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('list')
    return render(request, 'confirm_delete.html', {'object': room})
