from rest_framework import serializers
from .models import MediaAsset
from tkh_lexicon.serializers import TechniqueSerializer
from tkh_patterns.serializers import TulSerializer


class MediaAssetSerializer(serializers.ModelSerializer):
    techniques = TechniqueSerializer(many=True, read_only=True)
    tuls = TulSerializer(many=True, read_only=True)
    class Meta:
        model = MediaAsset
        fields = [
            "id",
            "file",
            "kind",
            "codec",
            "resolutions",
            "duration",
            "thumbnails",
            "status",
            "meta",
            "created_at",
            "updated_at",
            "techniques",
            "tuls",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "status"]


class PresignUploadRequestSerializer(serializers.Serializer):
    filename = serializers.CharField()


class MediaCompleteRequestSerializer(serializers.Serializer):
    key = serializers.CharField()
    kind = serializers.ChoiceField(choices=["video", "image", "audio"], default="video")


class PresignUploadResponseSerializer(serializers.Serializer):
    url = serializers.CharField()
    fields = serializers.DictField()

