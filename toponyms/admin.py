from django.contrib import admin
from .models import Toponym

@admin.register(Toponym)
class ToponymAdmin(admin.ModelAdmin):
    list_display = ('name_rus', 'name_bash', 'type', 'status', 'created_at')
    list_filter = ('status', 'type')
    search_fields = ('name_rus', 'name_bash', 'description')
    readonly_fields = ('created_at', 'updated_at')