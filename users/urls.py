from django.contrib.auth import views as auth_views
from django.urls import path
from .views import UserLoginView, UserLogoutView, UserPasswordChangeView, UserPasswordResetView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"), path("logout/", UserLogoutView.as_view(), name="logout"),
    path("senha/alterar/", UserPasswordChangeView.as_view(), name="password_change"),
    path("senha/resetar/", UserPasswordResetView.as_view(), name="password_reset"),
    path("senha/resetar/enviado/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("senha/resetar/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html", success_url="/login/"), name="password_reset_confirm"),
]
