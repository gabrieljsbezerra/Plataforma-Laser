from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from .forms import LoginForm

class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")

class UserPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("dashboard")

class UserPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.txt"
    success_url = reverse_lazy("password_reset_done")
