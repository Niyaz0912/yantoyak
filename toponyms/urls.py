from django.urls import path
from .views import MapView, ToponymDetailView

app_name = 'toponyms'

urlpatterns = [
    path('', MapView.as_view(), name='map'),
    path('<int:pk>/', ToponymDetailView.as_view(), name='detail'),
]