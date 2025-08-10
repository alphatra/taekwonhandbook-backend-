from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import Progress
from .serializers import ProgressSerializer


class ProgressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """User progress upsert and listing.

    PL: Idempotentny upsert postępu nauki użytkownika oraz listowanie własnego
    postępu. Tworzenie/aktualizacja łączy się po `(user,item_type,item_id)` i
    stosuje prostą politykę merge (nie zmniejszamy wyniku/streaku).

    EN: Idempotent upsert of the user's learning progress and listing of own
    records. Matched by `(user,item_type,item_id)` with merge policy that avoids
    decreasing `score`/`streaks`.
    """
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "progress"

    # get_queryset already defined above; keep single definition

    def get_queryset(self):
        # Avoid accessing request.user during schema generation
        if getattr(self, "swagger_fake_view", False):  # drf-spectacular
            return Progress.objects.none()
        return Progress.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        payload = request.data
        defaults = {
            "status": payload.get("status", "seen"),
            "score": max(0.0, float(payload.get("score", 0.0))),
            "streaks": max(0, int(payload.get("streaks", 0))),
            "meta": payload.get("meta", {}),
        }
        obj, created = Progress.objects.update_or_create(
            user=request.user,
            item_type=payload["item_type"],
            item_id=payload["item_id"],
            defaults=defaults,
        )
        # Merge policy example: ensure score/streaks are not decreased inadvertently
        if not created:
            changed = False
            if obj.score < float(payload.get("score", obj.score)):
                obj.score = float(payload.get("score", obj.score))
                changed = True
            if obj.streaks < int(payload.get("streaks", obj.streaks)):
                obj.streaks = int(payload.get("streaks", obj.streaks))
                changed = True
            if changed:
                obj.save(update_fields=["score", "streaks"]) 

        serializer = self.get_serializer(obj)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

# Create your views here.
