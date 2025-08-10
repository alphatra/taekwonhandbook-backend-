from __future__ import annotations

import json
from typing import Any, Dict, List

from django import template
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate

from tkh_billing.models import AdPolicy, Plan, Subscription
from tkh_lexicon.models import Technique
from tkh_media.models import MediaAsset
from tkh_patterns.models import Tul


register = template.Library()


@register.simple_tag
def admin_stats_payload() -> str:
    """Return aggregated stats as JSON for the admin dashboard charts."""
    payload: Dict[str, Any] = {
        "content": {
            "techniques": Technique.objects.count(),
            "tuls": Tul.objects.count(),
        },
        "media": {
            "ready": MediaAsset.objects.filter(status="ready").count(),
            "processing": MediaAsset.objects.filter(status="processing").count(),
            "uploaded": MediaAsset.objects.filter(status="uploaded").count(),
            "failed": MediaAsset.objects.filter(status="failed").count(),
        },
        "billing": {
            "plans": Plan.objects.count(),
            "subs_active": Subscription.objects.filter(status="active").count(),
        },
        "ads": {
            "avg_today": float(AdPolicy.objects.all().aggregate_avg_today() if hasattr(AdPolicy.objects, "aggregate_avg_today") else 0.0),
        },
    }
    # Fallback avg_today without custom manager method
    if payload["ads"]["avg_today"] == 0.0:
        agg = AdPolicy.objects.all().values_list("today_shown", flat=True)
        values = list(agg)
        payload["ads"]["avg_today"] = (sum(values) / len(values)) if values else 0.0

    # Time series last 30 days
    today = timezone.now().date()
    days: List[str] = [(today - timezone.timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
    # Media uploads per day
    media_qs = (
        MediaAsset.objects.annotate(d=TruncDate("created_at"))
        .values("d")
        .annotate(c=Count("id"))
    )
    media_map = {str(row["d"]): int(row["c"]) for row in media_qs}
    uploads_series = [media_map.get(day, 0) for day in days]
    # Subscriptions per day
    subs_qs = (
        Subscription.objects.annotate(d=TruncDate("created_at"))
        .values("d")
        .annotate(c=Count("id"))
    )
    subs_map = {str(row["d"]): int(row["c"]) for row in subs_qs}
    subs_series = [subs_map.get(day, 0) for day in days]

    payload["timeseries"] = {
        "labels": days,
        "uploads": uploads_series,
        "subs": subs_series,
    }
    return mark_safe(json.dumps(payload))

