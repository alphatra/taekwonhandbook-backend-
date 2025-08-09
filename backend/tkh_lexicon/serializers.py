from rest_framework import serializers

from .models import Technique


class TechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technique
        fields = [
            "id",
            "names",
            "audio",
            "category",
            "min_belt",
            "key_points",
            "common_mistakes",
            "videos",
            "safety",
            "tags",
            "version",
            "valid_from",
            "valid_to",
            "is_draft",
        ]

