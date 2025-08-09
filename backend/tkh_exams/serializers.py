from rest_framework import serializers
from tkh_lexicon.serializers import TechniqueSerializer
from tkh_patterns.serializers import TulSerializer

from .models import ExamSyllabus


class ExamSyllabusSerializer(serializers.ModelSerializer):
    required_techniques = TechniqueSerializer(many=True, read_only=True)
    required_tuls = TulSerializer(many=True, read_only=True)
    class Meta:
        model = ExamSyllabus
        fields = [
            "belt",
            "required_techniques",
            "required_tuls",
            "strength_tests",
            "theory_qs",
            "version",
            "valid_from",
            "valid_to",
            "is_draft",
        ]


class BeltPathSerializer(serializers.Serializer):
    belt = serializers.IntegerField()

