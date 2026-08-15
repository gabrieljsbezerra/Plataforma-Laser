from django.test import TestCase
from django.urls import reverse

class AuthenticationTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/login/?next=/dashboard/")
