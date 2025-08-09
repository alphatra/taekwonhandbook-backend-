import random

from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import QuizQuestion, QuizSession
from .serializers import (
    QuizAnswerRequestSerializer,
    QuizAnswerResponseSerializer,
    QuizQuestionSerializer,
    QuizSessionSerializer,
    QuizStartRequestSerializer,
)


@extend_schema(request=QuizStartRequestSerializer, responses=QuizSessionSerializer)
class QuizStartView(views.APIView):
    """Start a quiz session for the user.

    PL: Tworzy nową sesję quizu (tryb, opcjonalny pas), losuje pytania i
    zwraca stan sesji. Throttling per-scope, auth wymagane.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "quizzes"
    class DummySerializer:
        pass
    serializer_class = DummySerializer

    def get(self, request):
        mode = request.GET.get("mode", "terms")
        belt = request.GET.get("belt")
        qs = QuizQuestion.objects.filter(type=mode)
        if belt:
            qs = qs.filter(belt=belt)
        ids = list(qs.values_list("id", flat=True)[:10])
        random.shuffle(ids)
        session = QuizSession.objects.create(user=request.user, mode=mode, belt=belt or None, questions=ids)
        return Response(QuizSessionSerializer(session).data)


@extend_schema(request=QuizAnswerRequestSerializer, responses=QuizAnswerResponseSerializer)
class QuizAnswerView(views.APIView):
    """Answer a quiz question and advance the session.

    PL: Przetwarza odpowiedź użytkownika na bieżące pytanie, aktualizuje
    licznik poprawnych odpowiedzi i przesuwa wskaźnik. Zwraca stan sesji
    oraz dane pytania (dla klienta).
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "quizzes"
    class DummySerializer:
        pass
    serializer_class = DummySerializer

    def post(self, request, session_id: int):
        try:
            session = QuizSession.objects.get(id=session_id, user=request.user)
        except QuizSession.DoesNotExist:
            return Response({"detail": "not found"}, status=404)
        if session.finished:
            return Response(QuizSessionSerializer(session).data)
        if session.current_index >= len(session.questions):
            session.finished = True
            session.save(update_fields=["finished"])
            return Response(QuizSessionSerializer(session).data)

        qid = session.questions[session.current_index]
        try:
            q = QuizQuestion.objects.get(id=qid)
        except QuizQuestion.DoesNotExist:
            # skip broken question
            session.current_index += 1
            session.save(update_fields=["current_index"])
            return Response(QuizSessionSerializer(session).data)

        answer = int(request.data.get("answer", -1))
        if answer == q.correct:
            session.correct_count += 1
        session.current_index += 1
        if session.current_index >= len(session.questions):
            session.finished = True
        session.save(update_fields=["correct_count", "current_index", "finished"])
        return Response({
            "session": QuizSessionSerializer(session).data,
            "question": QuizQuestionSerializer(q).data,
            "isCorrect": answer == q.correct,
        }, status=status.HTTP_200_OK)


# Create your views here.
