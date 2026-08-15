from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class PlatformUserAdmin(UserAdmin):
    list_display = ("username", "email", "tenant", "role", "is_active")
    list_filter = ("role", "is_active", "tenant")
    fieldsets = UserAdmin.fieldsets + (("Plataforma", {"fields": ("tenant", "role")}),)
