from rest_framework import serializers

from .models import Club, ClubMember, Entitlement, Plan, Subscription


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

class ClubSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "plan",
            "seats_total",
            "seats_used",
            "logo_url",
            "created_at",
            "updated_at",
        ]


class ClubMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubMember
        fields = ["club", "user", "role", "created_at"]