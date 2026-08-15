from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Tenant

class User(AbstractUser):
    class Role(models.TextChoices):
        MASTER = "master", "Master"
        USER = "user", "Usuário"
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, related_name="users", null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=True)

    @property
    def is_master(self):
        return self.role == self.Role.MASTER or self.is_superuser
