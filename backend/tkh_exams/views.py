from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ExamSyllabus
from .serializers import ExamSyllabusSerializer, BeltPathSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample


@extend_schema(responses=ExamSyllabusSerializer)
class ExamSyllabusView(views.APIView):
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
