# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # ← добавили
    path('maps/', include('maps.urls')),
    path('', include('toponyms.urls')),
]