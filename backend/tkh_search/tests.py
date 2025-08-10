from django.test import Client, TestCase
from tkh_patterns.models import Tul


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Tul.objects.create(name="Do San", belt=7)
        Tul.objects.create(name="Hwa Rang", belt=3)

    def test_db_fallback(self):
        resp = self.client.get("/api/v1/search?q=Hwa&type=tul&limit=1")
        self.assertEqual(resp.status_code, 200)
        data = resp.json().get("results", [])
        self.assertEqual(len(data), 1)
        self.assertIn("Hwa", data[0]["name"])

# Create your tests here.
