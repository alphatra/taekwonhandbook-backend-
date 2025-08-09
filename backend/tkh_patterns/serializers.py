from rest_framework import serializers
from .models import Tul


class TulSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tul
        fields = [
            "id",
            "name",
            "belt",
            "steps",
            "diagram",
            "tempo",
            "videos",
            "meaning",
            "judge_notes",
            "version",
            "valid_from",
            "valid_to",
            "is_draft",
        ]

