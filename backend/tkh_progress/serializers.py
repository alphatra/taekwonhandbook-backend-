from rest_framework import serializers

from .models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = [
            "id",
            "user",
            "item_type",
            "item_id",
            "status",
            "score",
            "streaks",
            "last_seen_at",
            "meta",
        ]
        read_only_fields = ["id", "last_seen_at", "user"]

