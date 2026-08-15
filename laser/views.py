from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import ProcedureForm, SessionForm
from .models import LaserSession, Procedure
class ProcedureListView(LoginRequiredMixin, ListView):
    model = Procedure; template_name = "laser/list.html"; context_object_name = "procedures"
    def get_queryset(self): return Procedure.objects.filter(tenant=self.request.tenant).select_related("client", "procedure_type").prefetch_related("sessions")
class ProcedureCreateView(LoginRequiredMixin, CreateView):
    model = Procedure; form_class = ProcedureForm; template_name = "laser/form.html"; success_url = reverse_lazy("laser:list")
    def get_form(self, form_class=None):
        form = super().get_form(form_class); form.fields["client"].queryset = form.fields["client"].queryset.filter(tenant=self.request.tenant); form.fields["procedure_type"].queryset = form.fields["procedure_type"].queryset.filter(tenant=self.request.tenant); return form
    def form_valid(self, form): form.instance.tenant = self.request.tenant; return super().form_valid(form)

class ProcedureUpdateView(LoginRequiredMixin, UpdateView):
    model = Procedure; form_class = ProcedureForm; template_name = "laser/form.html"; success_url = reverse_lazy("laser:list")
    def get_queryset(self): return Procedure.objects.filter(tenant=self.request.tenant)
    def get_form(self, form_class=None):
        form = super().get_form(form_class); form.fields["client"].queryset = form.fields["client"].queryset.filter(tenant=self.request.tenant); form.fields["procedure_type"].queryset = form.fields["procedure_type"].queryset.filter(tenant=self.request.tenant); return form
    def form_valid(self, form):
        messages.success(self.request, "Procedimento atualizado com sucesso.")
        return super().form_valid(form)

class ProcedureDeleteView(LoginRequiredMixin, DeleteView):
    model = Procedure; template_name = "laser/confirm_delete.html"; success_url = reverse_lazy("laser:list")
    def get_queryset(self): return Procedure.objects.filter(tenant=self.request.tenant)
    def form_valid(self, form):
        messages.success(self.request, "Procedimento excluído com sucesso.")
        return super().form_valid(form)

class ProcedureDetailView(LoginRequiredMixin, DetailView):
    model = Procedure; template_name = "laser/detail.html"; context_object_name = "procedure"
    def get_queryset(self): return Procedure.objects.filter(tenant=self.request.tenant).select_related("client", "procedure_type").prefetch_related("sessions__operator")

class SessionCreateView(LoginRequiredMixin, CreateView):
    model = LaserSession; form_class = SessionForm; template_name = "laser/session_form.html"
    def dispatch(self, request, *args, **kwargs):
        self.procedure = Procedure.objects.filter(pk=kwargs["procedure_pk"], tenant=request.tenant).first()
        if self.procedure is None: from django.http import Http404; raise Http404
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs): return {**super().get_context_data(**kwargs), "procedure": self.procedure}
    def form_valid(self, form):
        form.instance.procedure = self.procedure; form.instance.operator = self.request.user
        messages.success(self.request, "Sessão adicionada com sucesso."); return super().form_valid(form)
    def get_success_url(self): return reverse_lazy("laser:detail", kwargs={"pk": self.procedure.pk})

class SessionUpdateView(LoginRequiredMixin, UpdateView):
    model = LaserSession; form_class = SessionForm; template_name = "laser/session_form.html"
    def get_queryset(self): return LaserSession.objects.filter(procedure__tenant=self.request.tenant).select_related("procedure")
    def get_context_data(self, **kwargs): return {**super().get_context_data(**kwargs), "procedure": self.object.procedure}
    def get_success_url(self): return reverse_lazy("laser:detail", kwargs={"pk": self.object.procedure.pk})

class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = LaserSession; template_name = "laser/session_confirm_delete.html"
    def get_queryset(self): return LaserSession.objects.filter(procedure__tenant=self.request.tenant).select_related("procedure")
    def get_success_url(self): return reverse_lazy("laser:detail", kwargs={"pk": self.object.procedure.pk})
