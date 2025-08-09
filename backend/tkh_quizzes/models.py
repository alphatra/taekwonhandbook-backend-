from django.conf import settings
from django.db import models


class QuizQuestion(models.Model):
    TYPE_CHOICES = (
        ("terms", "Terms"),
        ("techniques", "Techniques"),
        ("tul", "Tul"),
        ("theory", "Theory"),
    )

    type = models.CharField(max_length=24, choices=TYPE_CHOICES)
    belt = models.IntegerField(null=True, blank=True)
    payload = models.JSONField(default=dict)  # e.g. {prompt, refs}
    answers = models.JSONField(default=list)  # list of strings/options
    correct = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.type}:{self.id}"


class QuizSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode = models.CharField(max_length=24)
    belt = models.IntegerField(null=True, blank=True)
    questions = models.JSONField(default=list)  # list of question IDs
    current_index = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"session:{self.id}:{self.mode}"

# Create your models here.
