from django.contrib.auth import get_user_model
from tenants.models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        if request.user.is_authenticated:
            tenant_id = request.session.get("tenant_id")
            if tenant_id:
                request.tenant = Tenant.objects.filter(id=tenant_id, users=request.user, is_active=True).first()
            if request.tenant is None:
                request.tenant = request.user.tenant
                if request.tenant:
                    request.session["tenant_id"] = request.tenant.id
        return self.get_response(request)
