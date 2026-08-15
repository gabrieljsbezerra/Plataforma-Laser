from django import forms
from .models import Client
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ["tenant"]
        labels = {"name": "Nome completo", "phone": "Celular", "document": "CPF/RG", "birth_date": "Data de nascimento", "sex": "Sexo", "email": "E-mail", "photo": "Foto", "cep": "CEP", "address": "Endereço", "number": "Número", "complement": "Complemento", "neighborhood": "Bairro", "city": "Cidade", "state": "Estado", "notes": "Observações", "is_active": "Cliente ativo"}
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"}), "notes": forms.Textarea(attrs={"rows": 3})}
