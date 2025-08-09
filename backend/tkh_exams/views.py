from drf_spectacular.utils import extend_schema
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ExamSyllabus
from .serializers import ExamSyllabusSerializer


@extend_schema(responses=ExamSyllabusSerializer)
class ExamSyllabusView(views.APIView):
    """Return published exam syllabus for a given belt.

    PL: Zwraca opublikowany sylabus egzaminacyjny dla podanego pasa (`belt`).
    """
    permission_classes = [AllowAny]
    class DummySerializer:
        pass
    serializer_class = DummySerializer

    def get(self, request, belt: int):
        try:
            s = ExamSyllabus.objects.get(belt=belt, is_draft=False)
        except ExamSyllabus.DoesNotExist:
            return Response({"detail": "not found"}, status=404)
        return Response(ExamSyllabusSerializer(s).data)


# Create your views here.
