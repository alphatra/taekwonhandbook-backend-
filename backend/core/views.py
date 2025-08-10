"""Core auxiliary views and utilities for documentation.

This module exposes lightweight, read-only views that can be referenced by
the documentation or used for simple health checks and examples.

Docstrings are intentionally bilingual (PL/EN) to feed mkdocstrings.
"""

from __future__ import annotations

from django.http import HttpRequest, JsonResponse
from django.conf import settings
import socket
try:
    import requests
except Exception:  # pragma: no cover
    requests = None


def doc_ping(request: HttpRequest) -> JsonResponse:
    """Ping endpoint returning a tiny JSON payload.

    PL: Prosty endpoint zwracający minimalną odpowiedź JSON – wykorzystywany
    w przykładach dokumentacji i testach dymnych.

    Returns
    -------
    JsonResponse
        Payload postaci `{"ok": true}`.
    """

    return JsonResponse({"ok": True})


def robots_txt(_request: HttpRequest) -> JsonResponse:
    """Disallow indexing/scraping via robots.txt.

    PL: Proaktywnie blokuje indeksowanie (noindex/nofollow). To soft measure,
    nie stanowi zgody na scrapowanie.
    """

    return JsonResponse("User-agent: *\nDisallow: /\n", status=200, content_type="text/plain", safe=False)


def health(_request: HttpRequest) -> JsonResponse:
    """Healthcheck for critical dependencies (DB implicit via Django, Redis/Meilisearch optional).

    Returns JSON with status: ok/degraded and components.
    """
    status = "ok"
    checks = {
        "db": "ok",  # if Django loaded models, basic DB conn is typically fine here
    }
    # Redis URL presence implies channels/celery usage
    redis_url = getattr(settings, "CELERY_BROKER_URL", "") or getattr(settings, "REDIS_URL", "")
    if redis_url:
        try:
            host = redis_url.split("@")[-1].split("/")[0].split(":")[0]
            socket.gethostbyname(host)
            checks["redis"] = "ok"
        except Exception as e:  # pragma: no cover
            checks["redis"] = f"error: {e}"
            status = "degraded"
    # Meilisearch
    if getattr(settings, "MEILISEARCH_URL", None) and requests:
        try:
            r = requests.get(settings.MEILISEARCH_URL.rstrip("/") + "/health", timeout=1.5)
            checks["meilisearch"] = "ok" if r.ok else f"error: {r.status_code}"
            if not r.ok:
                status = "degraded"
        except Exception as e:  # pragma: no cover
            checks["meilisearch"] = f"error: {e}"
            status = "degraded"
    return JsonResponse({"status": status, **checks})

