from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [path("", RedirectView.as_view(pattern_name="dashboard", permanent=False), name="home"), path("admin/", admin.site.urls), path("", include("users.urls")), path("dashboard/", include("dashboard.urls")), path("clientes/", include("clients.urls")), path("laser/", include("laser.urls"))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
