from django.core.validators import MinValueValidator
from django.db import models
from clients.models import Client
from tenants.models import Tenant
from users.models import User

class ProcedureType(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="procedure_types")
    name = models.CharField("nome", max_length=120); is_active = models.BooleanField("ativo", default=True)
    class Meta: unique_together = [("tenant", "name")]; ordering = ["name"]
    def __str__(self): return self.name

class Procedure(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="procedures")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="procedures")
    procedure_type = models.ForeignKey(ProcedureType, on_delete=models.PROTECT, related_name="procedures")
    notes = models.TextField("observações", blank=True); created_at = models.DateTimeField("cadastrado em", auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.procedure_type} — {self.client}"

class LaserSession(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="sessions")
    number = models.PositiveIntegerField("número da sessão", validators=[MinValueValidator(1)])
    date = models.DateField("data"); region = models.CharField("região", max_length=120); equipment = models.CharField("equipamento", max_length=120, blank=True)
    wavelength = models.DecimalField("comprimento de onda (nm)", max_digits=7, decimal_places=2, null=True, blank=True); fluence = models.DecimalField("fluência", max_digits=7, decimal_places=2, null=True, blank=True)
    frequency = models.DecimalField("frequência", max_digits=7, decimal_places=2, null=True, blank=True); spot_size = models.DecimalField("spot size", max_digits=7, decimal_places=2, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField("duração (minutos)", null=True, blank=True); operator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="laser_sessions", verbose_name="operador"); observations = models.TextField("observações", blank=True)
    class Meta:
        ordering = ["-date", "-number"]; constraints = [models.UniqueConstraint(fields=["procedure", "number"], name="unique_session_number")]
