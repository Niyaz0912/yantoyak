# maps/urls.py
from django.urls import path
from .views import UserMapCreateView, UserMapDetailView

app_name = 'maps'

urlpatterns = [
    path('create/', UserMapCreateView.as_view(), name='create'),
    path('<slug:slug>/', UserMapDetailView.as_view(), name='detail'),
    path('', UserMapCreateView.as_view(), name='map_list'),
]