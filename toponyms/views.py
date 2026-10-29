# toponyms/views.py
from django.views.generic import TemplateView, DetailView
from django.db.models import Count
from .models import Toponym
from maps.models import UserMap


class MapView(TemplateView):
    template_name = 'toponyms/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['toponyms'] = Toponym.objects.filter(status='published').order_by('id')[:12]
        context['total_in_db'] = Toponym.objects.filter(status='published').count()
        context['google_maps_count'] = 3867

        if self.request.user.is_authenticated:
            context['user_maps'] = UserMap.objects.filter(owner=self.request.user)
        else:
            context['user_maps'] = UserMap.objects.none()

        return context


class ToponymDetailView(DetailView):
    model = Toponym
    template_name = 'toponyms/detail.html'
    context_object_name = 'toponym'

    def get_queryset(self):
        return Toponym.objects.filter(status='published')