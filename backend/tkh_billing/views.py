from __future__ import annotations

from datetime import timedelta

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

