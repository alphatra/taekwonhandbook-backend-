import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Tul
from .serializers import TulSerializer


class TulFilterSet(django_filters.FilterSet):
    hasMedia = django_filters.BooleanFilter(method="filter_has_media")

    def filter_has_media(self, queryset, name, value):  # noqa: ARG002
        if value is True:
            return queryset.filter(media_assets__isnull=False).distinct()
        if value is False:
            return queryset.filter(media_assets__isnull=True)
        return queryset

    class Meta:
        model = Tul
        fields = ["belt", "hasMedia"]


class TulViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only listing of tuls (patterns).

    PL: Endpoint publiczny (tylko odczyt) dla układów tul. Umożliwia filtrowanie
    po `belt` i opcjonalnie `hasMedia`, wyszukiwanie po nazwie oraz sortowanie.

    EN: Public read-only endpoint for patterns with filtering by `belt`, optional
    `hasMedia` flag, search by `name` and ordering.
    """
    queryset = Tul.objects.all()
    serializer_class = TulSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TulFilterSet
    search_fields = ["name"]
    ordering = ["belt", "name"]
    ordering_fields = ["belt", "name", "id"]

# Create your views here.
