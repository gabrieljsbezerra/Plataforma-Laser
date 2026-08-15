from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="E-mail ou usuário", widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"}))
    password = forms.CharField(label="Senha", strip=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
