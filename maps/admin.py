from django.contrib import admin
from .models import UserMap


@admin.register(UserMap)
class UserMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    filter_horizontal = ('toponyms',)  # удобный виджет для ManyToMany
    readonly_fields = ('created_at', 'updated_at')