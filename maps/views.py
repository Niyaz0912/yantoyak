# maps/views.py
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserMap
from .forms import UserMapForm


class UserMapCreateView(LoginRequiredMixin, CreateView):
    model = UserMap
    form_class = UserMapForm
    template_name = 'maps/create_map.html'
    success_url = reverse_lazy('maps:map_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class UserMapDetailView(DetailView):
    model = UserMap
    template_name = 'maps/map_detail.html'
    context_object_name = 'map'
    slug_field = 'slug'
    slug_url_kwarg = 'slug' 