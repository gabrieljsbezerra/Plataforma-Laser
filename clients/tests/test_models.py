from django.test import TestCase
from tenants.models import Tenant
from users.models import User
from clients.models import Client

class ClientIsolationTests(TestCase):
    def test_client_belongs_to_tenant(self):
        tenant = Tenant.objects.create(name="Aurora", slug="aurora")
        User.objects.create_user(username="ana", password="strong-password", tenant=tenant)
        client = Client.objects.create(tenant=tenant, name="Maria Silva", phone="11999999999")
        self.assertEqual(client.tenant, tenant)
