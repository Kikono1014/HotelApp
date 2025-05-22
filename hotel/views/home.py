from django.views.generic import TemplateView

class HotelHomeView(TemplateView):
    template_name = 'index.html'