from django.urls import path

from .views import (
    ClubInviteView,
    ClubListCreateView,
    EntitlementsTokenView,
    MeBillingView,
    PlansView,
    RevenueCatWebhookView,
    ShouldShowAdView,
    StripeWebhookView,
)

urlpatterns = [
    path("billing/plans", PlansView.as_view()),
    path("billing/me", MeBillingView.as_view()),
    path("ads/should-show", ShouldShowAdView.as_view()),
    path("billing/entitlements/token", EntitlementsTokenView.as_view()),
    path("billing/clubs", ClubListCreateView.as_view()),
    path("billing/clubs/<int:club_id>/invite", ClubInviteView.as_view()),
    path("billing/webhooks/stripe", StripeWebhookView.as_view()),
    path("billing/webhooks/revenuecat", RevenueCatWebhookView.as_view()),
]

