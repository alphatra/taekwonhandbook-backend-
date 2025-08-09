from __future__ import annotations

import hmac
import json
import os
from datetime import timedelta

from django.core import signing
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import AdPolicy, Entitlement, Plan, Subscription
from .serializers import EntitlementSerializer, PlanSerializer, SubscriptionSerializer


class PlansView(APIView):
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    def get(self, _request):
        plans = Plan.objects.order_by("price_cents")
        return Response(PlanSerializer(plans, many=True).data)


class MeBillingView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    def get(self, request):
        subs = Subscription.objects.filter(user=request.user, status="active").order_by("-updated_at")
        ents = Entitlement.objects.filter(user=request.user, active=True)
        payload = {
            "subscriptions": SubscriptionSerializer(subs, many=True).data,
            "entitlements": EntitlementSerializer(ents, many=True).data,
        }
        return Response(payload)


class ShouldShowAdView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "ads"

    def get(self, request):
        # no ads if entitlement active
        if Entitlement.objects.filter(user=request.user, key="no_ads", active=True).exists():
            return Response({"shouldShow": False, "reason": "no_ads"})

        policy, _ = AdPolicy.objects.get_or_create(user=request.user)
        now = timezone.now()
        if policy.last_shown_at and policy.last_shown_at.date() != now.date():
            policy.today_shown = 0
        # crude session cap; in real app reset per app-start
        if policy.today_shown >= policy.daily_cap or policy.session_shown >= policy.session_cap:
            return Response({"shouldShow": False, "reason": "cap"})
        # basic cooldown: min 2 min between fullscreen
        if policy.last_shown_at and now - policy.last_shown_at < timedelta(minutes=2):
            return Response({"shouldShow": False, "reason": "cooldown"})
        return Response({"shouldShow": True})


class EntitlementsTokenView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    def get(self, request):
        ents = Entitlement.objects.filter(user=request.user, active=True).values_list("key", flat=True)
        payload = {"uid": request.user.id, "entitlements": list(ents)}
        token = signing.dumps(payload, salt="entitlements")
        return Response({"token": token})


class StripeWebhookView(APIView):
    permission_classes = []
    throttle_classes = []

    def post(self, request):
        secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
        if secret:
            sig = request.headers.get("Stripe-Signature", "").encode()
            # Very simplified check: HMAC body with secret must equal header prefix (demo only)
            mac = hmac.new(secret.encode(), request.body, digestmod="sha256").hexdigest()
            if not mac or mac[:8].encode() not in sig:
                return Response({"detail": "invalid signature"}, status=400)
        try:
            event = json.loads(request.body.decode() or "{}")
        except Exception:
            return Response(status=400)
        # Demo: when event.type == 'customer.subscription.updated' toggle no_ads
        data = event.get("data", {}).get("object", {})
        user_id = data.get("metadata", {}).get("user_id")
        ent_keys = data.get("metadata", {}).get("entitlements", "no_ads").split(",")
        if user_id:
            for key in ent_keys:
                Entitlement.objects.update_or_create(user_id=user_id, key=key, defaults={"active": True})
        return Response({"ok": True})


class RevenueCatWebhookView(APIView):
    permission_classes = []
    throttle_classes = []

    def post(self, request):
        # Minimal: mark entitlements from payload
        try:
            payload = json.loads(request.body.decode() or "{}")
        except Exception:
            return Response(status=400)
        user_id = payload.get("app_user_id") or payload.get("subscriber", {}).get("app_user_id")
        entitlements = (
            payload.get("entitlements")
            or payload.get("subscriber", {}).get("entitlements", {})
            or {}
        )
        if user_id and isinstance(entitlements, dict):
            active = [k for k, v in entitlements.items() if v and v.get("active")]
            for key in active:
                Entitlement.objects.update_or_create(user_id=user_id, key=key, defaults={"active": True})
        return Response({"ok": True})

