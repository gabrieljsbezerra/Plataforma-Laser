from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "tenant", "is_active", "created_at")
    list_filter = ("tenant", "is_active")
    search_fields = ("name", "phone", "document", "email")
