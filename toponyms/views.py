from django.views.generic import TemplateView, DetailView  
from django.db.models import Count
from .models import Toponym

class MapView(TemplateView):
    template_name = 'toponyms/map.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Берем первые 12 по ID
        context['toponyms'] = Toponym.objects.filter(status='published').order_by('id')[:12]
        context['total_in_db'] = Toponym.objects.filter(status='published').count()
        context['google_maps_count'] = 3867
        return context
    
class ToponymDetailView(DetailView):
    model = Toponym
    template_name = 'toponyms/detail.html'
    context_object_name = 'toponym'
    
    def get_queryset(self):
        return Toponym.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно добавить связанные объекты, фото и т.д.
        return context