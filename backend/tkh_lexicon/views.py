import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Technique
from .serializers import TechniqueSerializer


class TechniqueFilterSet(django_filters.FilterSet):
    hasMedia = django_filters.BooleanFilter(method="filter_has_media")

    def filter_has_media(self, queryset, name, value):  # noqa: ARG002
        if value is True:
            return queryset.filter(media_assets__isnull=False).distinct()
        if value is False:
            return queryset.filter(media_assets__isnull=True)
        return queryset

    class Meta:
        model = Technique
        fields = ["category", "min_belt", "hasMedia"]


class TechniqueViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only listing of techniques.

    PL: Publiczny endpoint tylko do odczytu dla listy technik. Wspiera filtrowanie
    po `category`, minimalnym pasie (`min_belt`) oraz filtr `hasMedia`, a także
    wyszukiwanie pełnotekstowe po polu `names` i `tags`.

    EN: Public read-only endpoint for techniques with filters (`category`,
    `min_belt`, `hasMedia`) and search over `names` and `tags`.
    """
    queryset = Technique.objects.all()
    serializer_class = TechniqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TechniqueFilterSet
    search_fields = ["names", "tags"]
    ordering = ["-updated_at"]
    ordering_fields = ["updated_at", "min_belt", "id"]

# Create your views here.
