"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import json
import logging

from django.conf import settings
from django.contrib import admin
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import doc_ping

try:
    import meilisearch  # type: ignore
except Exception:  # pragma: no cover
    meilisearch = None
import redis as redis_lib
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def health(_request):
    logger = logging.getLogger("request")
    status = {"status": "ok"}
    # DB
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
            status["db"] = "ok"
    except Exception as e:
        status["db"] = f"error: {e}"
        status["status"] = "degraded"
    # Redis
    try:
        r = redis_lib.from_url(settings.REDIS_URL)
        r.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis"] = f"error: {e}"
        status["status"] = "degraded"
    # Meilisearch
    try:
        if meilisearch and getattr(settings, "MEILISEARCH_URL", None):
            client = meilisearch.Client(settings.MEILISEARCH_URL, settings.MEILISEARCH_API_KEY or None)
            client.health()
            status["meilisearch"] = "ok"
        else:
            status["meilisearch"] = "disabled"
    except Exception as e:
        status["meilisearch"] = f"error: {e}"
        status["status"] = "degraded"
    logger.info("health", extra={"health": json.dumps(status)})
    return JsonResponse(status)


def root(_request):
    html = """
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>ITF Taekwon-Do Handbook API</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; line-height: 1.5; }
      a { color: #2563eb; text-decoration: none; }
      a:hover { text-decoration: underline; }
      ul { margin: .5rem 0 0 1.25rem; }
      code { background: #f3f4f6; padding: .1rem .3rem; border-radius: .25rem; }
    </style>
    <link rel=\"icon\" href=\"/favicon.ico\" />
  </head>
  <body>
    <h1>ITF Taekwon-Do Handbook — Backend</h1>
    <p>Witaj! To landing strony API. Najważniejsze linki:</p>
    <ul>
      <li><a href=\"/api/docs/\">Swagger UI</a></li>
      <li><a href=\"/api/schema/\">OpenAPI JSON</a></li>
      <li><a href=\"/health/\">Health</a></li>
    </ul>
    <p>Kluczowe zasoby (v1):</p>
    <ul>
      <li><a href=\"/api/v1/techniques/\">/api/v1/techniques/</a></li>
      <li><a href=\"/api/v1/tuls/\">/api/v1/tuls/</a></li>
      <li><a href=\"/api/v1/search?q=Ap&type=technique\">/api/v1/search</a></li>
    </ul>
    <p>Auth (JWT): <code>POST /api/auth/token/</code></p>
  </body>
</html>
"""
    return HttpResponse(html)


def favicon(_request):
    # No favicon file yet; return empty 204 to avoid 404 noise
    return HttpResponse(status=204)

urlpatterns = [
    path("", root),
    path("favicon.ico", favicon),
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("ping/", doc_ping, name="ping"),
    path("api/v1/", include("tkh_lexicon.urls")),
    path("api/v1/", include("tkh_patterns.urls")),
    path("api/v1/", include("tkh_progress.urls")),
    path("api/v1/", include("tkh_media.urls")),
    path("api/v1/", include("tkh_search.urls")),
    path("api/v1/", include("tkh_quizzes.urls")),
    path("api/v1/", include("tkh_exams.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
