from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from .forms import ClientForm
from .models import Client

class TenantQueryMixin(LoginRequiredMixin):
    def get_queryset(self): return Client.objects.filter(tenant=self.request.tenant)
class ClientListView(TenantQueryMixin, ListView):
    model = Client; template_name = "clients/list.html"; context_object_name = "clients"; paginate_by = 12
    def get_queryset(self):
        queryset = super().get_queryset(); query = self.request.GET.get("q", "").strip(); status = self.request.GET.get("status", "all")
        if query: queryset = queryset.filter(Q(name__icontains=query) | Q(phone__icontains=query))
        if status == "active": queryset = queryset.filter(is_active=True)
        elif status == "inactive": queryset = queryset.filter(is_active=False)
        return queryset
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "selected_status": self.request.GET.get("status", "all")}
class ClientCreateView(TenantQueryMixin, CreateView):
    model = Client; form_class = ClientForm; template_name = "clients/form.html"; success_url = reverse_lazy("clients:list")
    def form_valid(self, form): form.instance.tenant = self.request.tenant; messages.success(self.request, "Cliente cadastrado com sucesso."); return super().form_valid(form)
class ClientUpdateView(TenantQueryMixin, UpdateView):
    model = Client; form_class = ClientForm; template_name = "clients/form.html"; success_url = reverse_lazy("clients:list")
class ClientDeleteView(TenantQueryMixin, DeleteView):
    model = Client; template_name = "clients/confirm_delete.html"; success_url = reverse_lazy("clients:list")
    def get_queryset(self): return super().get_queryset().filter(is_active=True)
    def form_valid(self, form):
        self.object.is_active = False
        self.object.save(update_fields=["is_active", "updated_at"])
        messages.success(self.request, "Cliente desativado com sucesso. O histórico de procedimentos foi preservado.")
        return HttpResponseRedirect(self.get_success_url())

class ClientReactivateView(TenantQueryMixin, View):
    def post(self, request, *args, **kwargs):
        client = self.get_queryset().filter(pk=kwargs["pk"], is_active=False).first()
        if client is None:
            from django.http import Http404
            raise Http404
        client.is_active = True
        client.save(update_fields=["is_active", "updated_at"])
        messages.success(request, "Cliente reativado com sucesso.")
        return HttpResponseRedirect(reverse_lazy("clients:list"))
