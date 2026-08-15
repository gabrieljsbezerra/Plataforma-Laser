from django.test import TestCase
from tenants.models import Tenant

class TenantModelTests(TestCase):
    def test_string_representation(self):
        tenant = Tenant.objects.create(name="Clínica Aurora", slug="clinica-aurora")
        self.assertEqual(str(tenant), "Clínica Aurora")
