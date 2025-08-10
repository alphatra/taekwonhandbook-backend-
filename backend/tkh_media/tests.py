from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class MediaPipelineTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user("u1", password="x")
        self.client = Client()
        self.client.force_login(self.user)

    def test_upload_complete_triggers_transcode(self):
        # complete without presign for simplicity
        resp = self.client.post(
            "/api/v1/media/complete",
            data={"key": "uploads/1/test.mp4", "kind": "video"},
        )
        self.assertIn(resp.status_code, (200, 201))
        data = resp.json()
        self.assertEqual(data.get("status"), "ready")  # eager Celery in DEBUG
        self.assertTrue(data.get("thumbnails"))

# Create your tests here.
