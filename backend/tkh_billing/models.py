from __future__ import annotations

from django.conf import settings
from django.db import models


class Plan(models.Model):
    code = models.CharField(max_length=32, unique=True)  # free|pro|club
    name = models.CharField(max_length=64)
    price_cents = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=8, default="PLN")
    trial_days = models.PositiveIntegerField(default=0)
    features = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.name


class Subscription(models.Model):
    PROVIDERS = [
        ("revenuecat", "RevenueCat"),
        ("stripe", "Stripe"),
        ("apple", "AppleIAP"),
        ("google", "GooglePlay"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    provider = models.CharField(max_length=16, choices=PROVIDERS)
    external_id = models.CharField(max_length=128, blank=True, default="")
    status = models.CharField(max_length=32, default="active")  # active|past_due|canceled
    current_period_end = models.DateTimeField(null=True, blank=True)
    seats = models.PositiveIntegerField(default=1)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Entitlement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)  # no_ads|quiz_create|club_creator|export_pdf
    active = models.BooleanField(default=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "key")]


class Club(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_clubs")
    name = models.CharField(max_length=80)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    seats_total = models.PositiveIntegerField(default=5)
    seats_used = models.PositiveIntegerField(default=1)
    logo_url = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClubMember(models.Model):
    ROLES = [("owner", "Owner"), ("coach", "Coach"), ("member", "Member")]
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLES, default="member")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("club", "user")]


class AdPolicy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    today_shown = models.PositiveIntegerField(default=0)
    session_shown = models.PositiveIntegerField(default=0)
    daily_cap = models.PositiveIntegerField(default=6)
    session_cap = models.PositiveIntegerField(default=3)
    last_shown_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def objects_with_avg(cls):  # type: ignore
        return cls.objects

    @classmethod
    def aggregate_avg_today(cls) -> float:
        vals = list(cls.objects.values_list("today_shown", flat=True))
        return (sum(vals) / len(vals)) if vals else 0.0


class WebhookEvent(models.Model):
    provider = models.CharField(max_length=16)  # stripe|revenuecat
    event_id = models.CharField(max_length=128)
    signature_valid = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = [("provider", "event_id")]

