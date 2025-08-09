import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import MediaAsset
from .serializers import (
    MediaAssetSerializer,
    MediaCompleteRequestSerializer,
    PresignUploadRequestSerializer,
    PresignUploadResponseSerializer,
)
from .tasks import transcode_media


@extend_schema(request=PresignUploadRequestSerializer, responses=PresignUploadResponseSerializer)
class MediaUploadView(views.APIView):
    """Generate a minimal S3/MinIO presigned POST for direct upload.

    PL: Generuje minimalny presigned POST (MinIO/S3) do bezpośredniego uploadu
    z klienta. Zabezpieczone JWT + throttlingiem. Parametr wejściowy: `filename`.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "media"
    class DummySerializer:
        pass
    serializer_class = DummySerializer

    def post(self, request):
        PresignUploadRequestSerializer(data=request.data).is_valid(raise_exception=True)
        # Minimalny presigned POST (kompatybilny z MinIO/S3, uproszczony)
        filename = request.data.get("filename")
        if not filename:
            return Response({"detail": "filename required"}, status=400)

        bucket = settings.S3_BUCKET if hasattr(settings, "S3_BUCKET") else "taekwonhandbook"
        key = f"uploads/{request.user.id}/{filename}"

        endpoint = getattr(settings, "S3_ENDPOINT_URL", "http://localhost:9000")
        access_key = getattr(settings, "S3_ACCESS_KEY", "minioadmin")
        secret_key = getattr(settings, "S3_SECRET_KEY", "minioadmin").encode()

        expires = (datetime.now(timezone.utc) + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        policy = {
            "expiration": expires,
            "conditions": [
                {"bucket": bucket},
                ["starts-with", "$key", key],
                {"acl": "private"},
                ["content-length-range", 0, 104857600],  # 100MB
            ],
        }
        policy_b64 = base64.b64encode(json.dumps(policy).encode()).decode()
        signature = base64.b64encode(hmac.new(secret_key, policy_b64.encode(), hashlib.sha1).digest()).decode()

        url = urljoin(endpoint + "/", f"{bucket}")
        return Response(
            {
                "url": url,
                "fields": {
                    "key": key,
                    "acl": "private",
                    "AWSAccessKeyId": access_key,
                    "policy": policy_b64,
                    "signature": signature,
                },
            }
        )


@extend_schema(request=MediaCompleteRequestSerializer, responses=MediaAssetSerializer)
class MediaCompleteView(views.APIView):
    """Finalize upload and trigger async transcode pipeline.

    PL: Finalizuje upload (tworzy rekord `MediaAsset`) i uruchamia asynchroniczny
    pipeline transkodowania (Celery). Zwraca metadane zasobu.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "media"
    class DummySerializer:
        pass
    serializer_class = DummySerializer

    def post(self, request):
        serializer = MediaAssetSerializer(data={
            "file": request.data.get("key"),
            "kind": request.data.get("kind", "video"),
            "status": "uploaded",
        })
        serializer.is_valid(raise_exception=True)
        asset = serializer.save()
        # uruchom pipeline transkodowania (w DEBUG domyślnie eager)
        transcode_media.delay(asset.id)
        asset.refresh_from_db()
        return Response(MediaAssetSerializer(asset).data, status=status.HTTP_201_CREATED)


class MediaAssetViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only access to processed media assets with filters/search."""
    queryset = MediaAsset.objects.all().order_by("-updated_at")
    serializer_class = MediaAssetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "kind": ["exact"],
        "status": ["exact"],
        "techniques": ["exact"],
        "tuls": ["exact"],
    }
    search_fields = ["file", "codec"]


# Create your views here.
