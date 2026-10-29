# maps/urls.py
from django.urls import path
from .views import UserMapCreateView, UserMapDetailView

app_name = 'maps'

urlpatterns = [
    path('create/', UserMapCreateView.as_view(), name='create'),
    path('<int:pk>/', UserMapDetailView.as_view(), name='detail'),  # ← добавили
    path('', UserMapCreateView.as_view(), name='map_list'),
]