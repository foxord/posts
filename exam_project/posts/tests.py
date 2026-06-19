# posts/tests.py
from django.test import TestCase


class HealthCheckTest(TestCase):
    def test_ping_endpoint(self):
        response = self.client.get('/posts/ping/')  # ← было '/ping/', добавьте префикс
        self.assertEqual(response.status_code, 200)