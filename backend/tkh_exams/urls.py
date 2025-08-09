from django.urls import path
from .views import ExamSyllabusView

urlpatterns = [
    path("exams/<int:belt>/syllabus", ExamSyllabusView.as_view(), name="exam-syllabus"),
]

