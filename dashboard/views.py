from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from clients.models import Client
from laser.models import LaserSession, Procedure
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs); tenant = self.request.tenant
        context.update(total_clients=Client.objects.filter(tenant=tenant, is_active=True).count(), total_procedures=Procedure.objects.filter(tenant=tenant).count(), total_sessions=LaserSession.objects.filter(procedure__tenant=tenant).count(), recent_clients=Client.objects.filter(tenant=tenant)[:5], recent_sessions=LaserSession.objects.filter(procedure__tenant=tenant).select_related("procedure__client")[:5]); return context
