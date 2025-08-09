from django.core.management.base import BaseCommand

from tkh_billing.models import Entitlement, Plan


class Command(BaseCommand):
    help = "Seed billing plans and default entitlements"

    def handle(self, *args, **options):
        plans = [
            {
                "code": "free",
                "name": "Free",
                "price_cents": 0,
                "currency": "PLN",
                "trial_days": 0,
                "features": {"ads": True},
            },
            {
                "code": "pro",
                "name": "Pro",
                "price_cents": 1499,
                "currency": "PLN",
                "trial_days": 7,
                "features": {"ads": False, "no_ads": True},
            },
            {
                "code": "club",
                "name": "Club",
                "price_cents": 5900,
                "currency": "PLN",
                "trial_days": 14,
                "features": {"ads": False, "no_ads": True, "club": True, "quiz_create": True},
            },
        ]
        for p in plans:
            Plan.objects.update_or_create(code=p["code"], defaults=p)
        self.stdout.write(self.style.SUCCESS("Seeded billing plans"))

