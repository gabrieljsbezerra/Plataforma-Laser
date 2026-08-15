from django.core.validators import FileExtensionValidator
from django.db import models
from tenants.models import Tenant

class Client(models.Model):
    class Sex(models.TextChoices):
        FEMALE = "F", "Feminino"
        MALE = "M", "Masculino"
        OTHER = "O", "Outro"
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField("nome", max_length=160)
    phone = models.CharField("celular", max_length=25)
    document = models.CharField("CPF/RG", max_length=30, blank=True)
    birth_date = models.DateField("data de nascimento", null=True, blank=True)
    sex = models.CharField("sexo", max_length=1, choices=Sex.choices, blank=True)
    email = models.EmailField("e-mail", blank=True)
    photo = models.ImageField("foto", upload_to="clients/%Y/%m/", blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])])
    cep = models.CharField("CEP", max_length=9, blank=True); address = models.CharField("endereço", max_length=180, blank=True)
    number = models.CharField("número", max_length=15, blank=True); complement = models.CharField("complemento", max_length=80, blank=True)
    neighborhood = models.CharField("bairro", max_length=100, blank=True); city = models.CharField("cidade", max_length=100, blank=True)
    state = models.CharField("estado", max_length=2, blank=True); notes = models.TextField("observações", blank=True)
    is_active = models.BooleanField("ativo", default=True); created_at = models.DateTimeField("cadastrado em", auto_now_add=True); updated_at = models.DateTimeField("atualizado em", auto_now=True)
    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["tenant", "name"]), models.Index(fields=["tenant", "phone"])]
    def __str__(self): return self.name
