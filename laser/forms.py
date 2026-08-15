from django import forms
from .models import LaserSession, Procedure
class ProcedureForm(forms.ModelForm):
    class Meta:
        model = Procedure; fields = ["client", "procedure_type", "notes"]
        labels = {"client": "Cliente", "procedure_type": "Tipo de procedimento", "notes": "Observações"}
class SessionForm(forms.ModelForm):
    class Meta:
        model = LaserSession; exclude = ["procedure", "operator"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}), "observations": forms.Textarea(attrs={"rows": 3})}
