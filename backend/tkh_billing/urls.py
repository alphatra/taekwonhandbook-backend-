from django.urls import path

from .views import MeBillingView, PlansView, ShouldShowAdView

urlpatterns = [
    path("billing/plans", PlansView.as_view()),
    path("billing/me", MeBillingView.as_view()),
    path("ads/should-show", ShouldShowAdView.as_view()),
]

