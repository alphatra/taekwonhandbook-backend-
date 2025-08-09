from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
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
    queryset = Tul.objects.all()
    serializer_class = TulSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TulFilterSet
    search_fields = ["name"]
    ordering = ["belt", "name"]
    ordering_fields = ["belt", "name", "id"]

# Create your views here.
