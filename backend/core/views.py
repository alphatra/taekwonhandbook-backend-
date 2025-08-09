"""Core auxiliary views and utilities for documentation.

This module exposes lightweight, read-only views that can be referenced by
the documentation or used for simple health checks and examples.

Docstrings are intentionally bilingual (PL/EN) to feed mkdocstrings.
"""

from __future__ import annotations

from django.http import HttpRequest, JsonResponse


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

