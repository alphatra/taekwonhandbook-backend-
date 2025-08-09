from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from tkh_lexicon.models import Technique
from tkh_patterns.models import Tul

try:
    import meilisearch  # type: ignore
except Exception:  # pragma: no cover
    meilisearch = None


from .serializers import SearchResponseSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name="q", description="Query string", required=False, type=str),
        OpenApiParameter(name="type", description="technique|tul", required=False, type=str),
    ],
    responses=SearchResponseSerializer,
)
class SearchView(APIView):
    """Unified search across techniques and tuls with Meilisearch fallback.

    PL: Zunifikowane wyszukiwanie (techniques/tuls). Najpierw Meilisearch,
    a w razie braku usługi – fallback do zapytań DB. Throttling per-scope.

    EN: Unified search with Meilisearch first, then database fallback.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "search"
    # For OpenAPI schema hints
    class DummySerializer:
        pass
    serializer_class = DummySerializer

    def get(self, request):
        query = request.GET.get("q", "").strip()
        kind = request.GET.get("type", "technique")
        results = []

        if meilisearch and getattr(settings, "MEILISEARCH_URL", None):
            try:
                client = meilisearch.Client(settings.MEILISEARCH_URL, settings.MEILISEARCH_API_KEY or None)
                index_name = "techniques" if kind == "technique" else "tuls"
                idx = client.index(index_name)
                res = idx.search(query or "", {"limit": 20})
                results = res.get("hits", [])
            except Exception:
                results = []

        if not results:  # fallback DB
            if kind == "technique":
                qs = Technique.objects.all()
                if query:
                    qs = qs.filter(category__icontains=query)
                results = [
                    {"id": t.id, "names": t.names, "category": t.category, "min_belt": t.min_belt}
                    for t in qs[:20]
                ]
            else:
                qs = Tul.objects.all()
                if query:
                    qs = qs.filter(name__icontains=query)
                results = [
                    {"id": x.id, "name": x.name, "belt": x.belt}
                    for x in qs[:20]
                ]

        return Response({"results": results})

# Create your views here.
