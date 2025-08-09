from django.urls import path
from .views import QuizStartView, QuizAnswerView

urlpatterns = [
    path("quizzes/start", QuizStartView.as_view(), name="quiz-start"),
    path("quizzes/<int:session_id>/answer", QuizAnswerView.as_view(), name="quiz-answer"),
]

