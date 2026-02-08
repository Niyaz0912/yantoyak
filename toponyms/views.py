from django.views.generic import ListView
from django.core.serializers import serialize
import json
from .models import Toponym

class MapView(ListView):
    model = Toponym
    template_name = 'toponyms/map.html'
    context_object_name = 'toponyms'
    
    def get_queryset(self):
        return Toponym.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Преобразуем QuerySet в JSON для карты
        toponyms_json = serialize('json', context['toponyms'])
        context['toponyms_json'] = toponyms_json
        return context