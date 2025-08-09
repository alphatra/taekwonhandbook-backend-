from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
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
    queryset = Technique.objects.all()
    serializer_class = TechniqueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TechniqueFilterSet
    search_fields = ["names", "tags"]
    ordering = ["-updated_at"]
    ordering_fields = ["updated_at", "min_belt", "id"]

# Create your views here.
