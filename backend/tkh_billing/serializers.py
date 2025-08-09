from rest_framework import serializers

from .models import Entitlement, Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["code", "name", "price_cents", "currency", "trial_days", "features"]


class EntitlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entitlement
        fields = ["key", "active"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = [
            "plan",
            "provider",
            "status",
            "current_period_end",
            "seats",
        ]

