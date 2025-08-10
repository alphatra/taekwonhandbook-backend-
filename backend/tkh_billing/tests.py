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

    def test_self_leave(self):
        # owner creates club and invites member; then member leaves
        User = get_user_model()
        owner = self.owner
        member = self.member
        self.client.force_login(owner)
        resp = self.client.post(
            "/api/v1/billing/clubs",
            data=json.dumps({"name": "Club B", "plan": "club", "seats_total": 2}),
            content_type="application/json",
        )
        club_id = resp.json()["id"]
        self.client.post(
            f"/api/v1/billing/clubs/{club_id}/invite",
            data=json.dumps({"user_id": member.id}),
            content_type="application/json",
        )
        # member leaves
        client2 = Client()
        client2.force_login(member)
        resp = client2.post(f"/api/v1/billing/clubs/{club_id}/leave")
        self.assertEqual(resp.status_code, 204)

    def test_list_filter_and_order(self):
        # create two clubs
        self.client.force_login(self.owner)
        resp = self.client.post(
            "/api/v1/billing/clubs",
            data=json.dumps({"name": "Zeta Club", "plan": "club", "seats_total": 2}),
            content_type="application/json",
        )
        resp = self.client.post(
            "/api/v1/billing/clubs",
            data=json.dumps({"name": "Alpha Dojang", "plan": "club", "seats_total": 2}),
            content_type="application/json",
        )
        # filter q=Alpha
        resp = self.client.get("/api/v1/billing/clubs?q=Alpha")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any("Alpha" in c["name"] for c in data))
        # ordering by name asc
        resp = self.client.get("/api/v1/billing/clubs?ordering=name")
        names = [c["name"] for c in resp.json()]
        self.assertEqual(names, sorted(names))

    def test_members_list_and_set_role(self):
        self.client.force_login(self.owner)
        # create club
        resp = self.client.post(
            "/api/v1/billing/clubs",
            data=json.dumps({"name": "Role Club", "plan": "club", "seats_total": 2}),
            content_type="application/json",
        )
        club_id = resp.json()["id"]
        # invite member
        self.client.post(
            f"/api/v1/billing/clubs/{club_id}/invite",
            data=json.dumps({"user_id": self.member.id}),
            content_type="application/json",
        )
        # list members
        resp = self.client.get(f"/api/v1/billing/clubs/{club_id}/members")
        self.assertEqual(resp.status_code, 200)
        members = resp.json()
        self.assertTrue(any(m["user"] == self.member.id for m in members))
        # set role
        resp = self.client.post(
            f"/api/v1/billing/clubs/{club_id}/members/{self.member.id}/role",
            data=json.dumps({"role": "coach"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["role"], "coach")


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

