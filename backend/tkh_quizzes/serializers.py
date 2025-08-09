from rest_framework import serializers
from .models import QuizQuestion, QuizSession


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ["id", "type", "belt", "payload", "answers", "correct"]


class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = [
            "id",
            "mode",
            "belt",
            "questions",
            "current_index",
            "correct_count",
            "finished",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "questions", "current_index", "correct_count", "finished"]


class QuizStartRequestSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=["terms", "techniques", "tul", "theory"], default="terms")
    belt = serializers.IntegerField(required=False)


class QuizAnswerRequestSerializer(serializers.Serializer):
    answer = serializers.IntegerField()


class QuizAnswerResponseSerializer(serializers.Serializer):
    session = QuizSessionSerializer()
    question = QuizQuestionSerializer()
    isCorrect = serializers.BooleanField()

