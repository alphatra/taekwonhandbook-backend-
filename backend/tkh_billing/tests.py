from __future__ import annotations

import json
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class ClubApiTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.owner = User.objects.create_user("owner", password="Owner123!")
        self.member = User.objects.create_user("member", password="Member123!")
        self.client = Client()
        self.client.force_login(self.owner)

    def test_create_and_invite_and_remove(self):
        resp = self.client.post(
            "/api/v1/billing/clubs",
            data=json.dumps({"name": "Club A", "plan": "club", "seats_total": 2}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)
        club_id = resp.json()["id"]
        resp = self.client.post(
            f"/api/v1/billing/clubs/{club_id}/invite",
            data=json.dumps({"user_id": self.member.id}),
            content_type="application/json",
        )
        self.assertIn(resp.status_code, (200, 201))
        resp = self.client.delete(f"/api/v1/billing/clubs/{club_id}/members/{self.member.id}")
        self.assertEqual(resp.status_code, 204)
        # now delete empty club
        resp = self.client.delete(f"/api/v1/billing/clubs/{club_id}")
        self.assertEqual(resp.status_code, 204)


class StripeWebhookTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user("u1", password="x")
        self.client = Client()

    def test_subscription_created_activates_entitlement(self):
        payload = {
            "id": "evt_test_unit_1",
            "type": "customer.subscription.created",
            "data": {
                "object": {"metadata": {"user_id": str(self.user.id), "entitlements": "no_ads"}}
            },
        }
        resp = self.client.post(
            "/api/v1/billing/webhooks/stripe", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.client.force_login(self.user)
        resp = self.client.get("/api/v1/billing/entitlements/token")
        self.assertEqual(resp.status_code, 200)
        token = resp.json().get("token", "")
        self.assertTrue(token)

