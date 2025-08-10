from __future__ import annotations

import hmac
import json
import os
from datetime import timedelta
from typing import Any, Dict

from django.core import signing
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema

from .models import AdPolicy, Club, ClubMember, Entitlement, Plan, Subscription, WebhookEvent
from .serializers import (
    ClubMemberSerializer,
    ClubSerializer,
    EntitlementSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)


class PlansView(APIView):
    """PL: Lista planów subskrypcyjnych (Free/Pro/Club).\n\nEN: List available subscription plans (Free/Pro/Club)."""
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["billing"], responses=OpenApiResponse(response=PlanSerializer(many=True)))
    def get(self, _request):
        plans = Plan.objects.order_by("price_cents")
        return Response(PlanSerializer(plans, many=True).data)


class MeBillingView(APIView):
    """PL: Moje subskrypcje i uprawnienia.\n\nEN: Current user's subscriptions and entitlements."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["billing"], responses={200: dict})
    def get(self, request):
        subs = Subscription.objects.filter(user=request.user, status="active").order_by("-updated_at")
        ents = Entitlement.objects.filter(user=request.user, active=True)
        payload = {
            "subscriptions": SubscriptionSerializer(subs, many=True).data,
            "entitlements": EntitlementSerializer(ents, many=True).data,
        }
        return Response(payload)


class ShouldShowAdView(APIView):
    """PL: Decyzja o wyświetleniu reklamy fullscreen z uwzględnieniem capów i entitlementów.\n\nEN: Server-side ad decision (caps/cooldown/no_ads entitlement)."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "ads"

    @extend_schema(tags=["ads"], responses={200: dict})
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
    """PL: Krótkotrwały token z listą uprawnień (TTL 5 min).\n\nEN: Short-lived entitlements token (5 min TTL)."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["billing"], responses={200: dict})
    def get(self, request):
        ents = Entitlement.objects.filter(user=request.user, active=True).values_list("key", flat=True)
        # krótkie TTL (5 min) i timestamp do walidacji po stronie klienta
        payload = {
            "uid": request.user.id,
            "entitlements": list(ents),
            "exp": int((timezone.now() + timedelta(minutes=5)).timestamp()),
        }
        token = signing.dumps(payload, salt="entitlements")
        return Response({"token": token, "ttlSeconds": 300})


class StripeWebhookView(APIView):
    """PL: Webhook Stripe (idempotencja, minimalne mapowanie zdarzeń).\n\nEN: Stripe webhook (idempotent, minimal event mapping)."""
    permission_classes = []
    throttle_classes = []

    @extend_schema(tags=["billing-webhooks"], request=None, responses={200: dict})
    def post(self, request):
        secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
        sig = request.headers.get("Stripe-Signature", "")
        signature_valid = False
        signature_hint = ""
        if secret and sig:
            mac = hmac.new(secret.encode(), request.body, digestmod="sha256").hexdigest()
            # uproszczona walidacja: porównanie prefiksu, w prod ucyj oficjalnej biblioteki Stripe
            signature_valid = mac[:16] in sig
            signature_hint = mac[:16]
        try:
            event: Dict[str, Any] = json.loads(request.body.decode() or "{}")
        except Exception:
            return Response(status=400)
        event_id = str(event.get("id") or signature_hint)
        if not event_id:
            return Response(status=400)
        obj, created = WebhookEvent.objects.get_or_create(
            provider="stripe",
            event_id=event_id,
            defaults={"payload": event, "signature_valid": bool(signature_valid)},
        )
        if not created:
            return Response({"ok": True, "duplicate": True})
        # Minimalne mapowanie typów zdarzeń → entitlements
        etype = event.get("type")
        data = (event.get("data") or {}).get("object", {})
        user_id = (data.get("metadata") or {}).get("user_id")
        ent_keys = (data.get("metadata") or {}).get("entitlements") or "no_ads"
        keys = [k for k in str(ent_keys).split(",") if k]
        if user_id and etype in {"customer.subscription.created", "customer.subscription.updated"}:
            for key in keys:
                Entitlement.objects.update_or_create(user_id=user_id, key=key, defaults={"active": True})
        if user_id and etype in {"customer.subscription.deleted", "customer.subscription.paused"}:
            for key in keys:
                Entitlement.objects.update_or_create(user_id=user_id, key=key, defaults={"active": False})
        obj.processed_at = timezone.now()
        obj.save(update_fields=["processed_at"]) 
        return Response({"ok": True})


class RevenueCatWebhookView(APIView):
    """PL: Webhook RevenueCat (prosta weryfikacja HMAC).\n\nEN: RevenueCat webhook (simple HMAC check)."""
    permission_classes = []
    throttle_classes = []

    @extend_schema(tags=["billing-webhooks"], request=None, responses={200: dict})
    def post(self, request):
        try:
            payload = json.loads(request.body.decode() or "{}")
        except Exception:
            return Response(status=400)
        # Prosta weryfikacja: opcjonalny nagłówek tajemnicy
        secret = os.getenv("REVENUECAT_WEBHOOK_SECRET", "")
        hdr = request.headers.get("X-Webhook-Signature", "")
        signature_valid = False
        if secret and hdr:
            mac = hmac.new(secret.encode(), request.body, digestmod="sha256").hexdigest()
            signature_valid = hdr.startswith(mac[:16])
        user_id = payload.get("app_user_id") or payload.get("subscriber", {}).get("app_user_id")
        entitlements = (
            payload.get("entitlements")
            or payload.get("subscriber", {}).get("entitlements", {})
            or {}
        )
        event_id = str(payload.get("event_id") or payload.get("id") or "")
        if not event_id:
            return Response(status=400)
        obj, created = WebhookEvent.objects.get_or_create(
            provider="revenuecat",
            event_id=event_id,
            defaults={"payload": payload, "signature_valid": bool(signature_valid)},
        )
        if not created:
            return Response({"ok": True, "duplicate": True})
        if user_id and isinstance(entitlements, dict):
            active = {k for k, v in entitlements.items() if v and v.get("active")}
            # ustaw aktywne na True, resztę zdezaktywuj
            all_keys = set(entitlements.keys())
            for key in all_keys:
                Entitlement.objects.update_or_create(
                    user_id=user_id, key=key, defaults={"active": key in active}
                )
        obj.processed_at = timezone.now()
        obj.save(update_fields=["processed_at"]) 
        return Response({"ok": True})


class ClubListCreateView(APIView):
    """PL: Lista i tworzenie klubów właściciela.\n\nEN: List and create owner clubs."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(
        tags=["clubs"],
        responses={200: ClubSerializer(many=True)},
        examples=[
            OpenApiExample(
                "ClubList",
                value=[
                    {
                        "id": 1,
                        "name": "Do jang A",
                        "plan": {"code": "club", "name": "Club", "price_cents": 5900, "currency": "PLN", "trial_days": 14, "features": {"no_ads": True, "club": True}},
                        "seats_total": 10,
                        "seats_used": 3,
                        "logo_url": "",
                        "created_at": "2025-08-09T23:38:24Z",
                        "updated_at": "2025-08-09T23:38:24Z",
                    }
                ],
            )
        ],
    )
    def get(self, request):
        clubs = Club.objects.filter(owner=request.user).order_by("-created_at")
        return Response(ClubSerializer(clubs, many=True).data)

    @extend_schema(
        tags=["clubs"],
        request=None,
        responses={201: ClubSerializer},
    )
    def post(self, request):
        name = str(request.data.get("name") or "").strip()
        plan_code = str(request.data.get("plan") or "club").strip()
        seats_total = int(request.data.get("seats_total") or 5)
        if not name:
            return Response({"detail": "name required"}, status=400)
        try:
            plan = Plan.objects.get(code=plan_code)
        except Plan.DoesNotExist:
            return Response({"detail": "invalid plan"}, status=400)
        max_seats = int((plan.features or {}).get("seats_max", 20))
        seats_total = min(max(seats_total, 1), max_seats)
        club = Club.objects.create(owner=request.user, name=name, plan=plan, seats_total=seats_total, seats_used=1)
        ClubMember.objects.create(club=club, user=request.user, role="owner")
        return Response(ClubSerializer(club).data, status=201)


class ClubInviteView(APIView):
    """PL: Zapraszanie użytkownika do klubu (owner only).\n\nEN: Invite user to club (owner only)."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["clubs"], request=None, responses={200: ClubMemberSerializer, 201: ClubMemberSerializer})
    def post(self, request, club_id: int):
        try:
            club = Club.objects.get(id=club_id, owner=request.user)
        except Club.DoesNotExist:
            return Response(status=404)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "user_id required"}, status=400)
        if club.seats_used >= club.seats_total:
            return Response({"detail": "no seats available"}, status=400)
        member, created = ClubMember.objects.get_or_create(club=club, user_id=user_id, defaults={"role": "member"})
        if created:
            club.seats_used += 1
            club.save(update_fields=["seats_used"]) 
        return Response(ClubMemberSerializer(member).data, status=201 if created else 200)


class ClubRemoveMemberView(APIView):
    """PL: Usuwanie członka (nie ownera) i zwolnienie miejsca.\n\nEN: Remove non-owner member and free seat."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["clubs"], responses={204: None})
    def delete(self, request, club_id: int, user_id: int):
        try:
            club = Club.objects.get(id=club_id, owner=request.user)
        except Club.DoesNotExist:
            return Response(status=404)
        try:
            member = ClubMember.objects.get(club=club, user_id=user_id)
        except ClubMember.DoesNotExist:
            return Response(status=404)
        # owner cannot be removed via this endpoint
        if member.role == "owner":
            return Response({"detail": "cannot remove owner"}, status=400)
        member.delete()
        if club.seats_used > 0:
            club.seats_used -= 1
            club.save(update_fields=["seats_used"]) 
        return Response(status=204)


class ClubDeleteView(APIView):
    """PL: Usuwanie klubu (dozwolone, gdy tylko owner jest członkiem).\n\nEN: Delete club (allowed when owner is the only member)."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["clubs"], responses={204: None, 400: dict, 404: None})
    def delete(self, request, club_id: int):
        try:
            club = Club.objects.get(id=club_id, owner=request.user)
        except Club.DoesNotExist:
            return Response(status=404)
        # can delete only when only owner remains
        member_count = ClubMember.objects.filter(club=club).count()
        if member_count > 1 or club.seats_used > 1:
            return Response({"detail": "cannot delete non-empty club"}, status=400)
        ClubMember.objects.filter(club=club).delete()
        club.delete()
        return Response(status=204)


class ClubSelfLeaveView(APIView):
    """PL: Członek sam opuszcza klub (nie owner).\n\nEN: Member leaves the club (non-owner)."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "billing"

    @extend_schema(tags=["clubs"], responses={204: None, 400: dict, 404: None})
    def post(self, request, club_id: int):
        try:
            club = Club.objects.get(id=club_id)
        except Club.DoesNotExist:
            return Response(status=404)
        try:
            member = ClubMember.objects.get(club=club, user=request.user)
        except ClubMember.DoesNotExist:
            return Response(status=404)
        if member.role == "owner":
            return Response({"detail": "owner cannot self-leave"}, status=400)
        member.delete()
        if club.seats_used > 0:
            club.seats_used -= 1
            club.save(update_fields=["seats_used"]) 
        return Response(status=204)

