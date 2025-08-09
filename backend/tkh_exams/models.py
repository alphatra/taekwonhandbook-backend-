from django.db import models
from tkh_lexicon.models import Technique
from tkh_patterns.models import Tul


class ExamSyllabus(models.Model):
    belt = models.IntegerField(unique=True, verbose_name="Pas")
    required_techniques = models.ManyToManyField(Technique, blank=True, related_name="exam_syllabuses", verbose_name="Wymagane techniki")
    required_tuls = models.ManyToManyField(Tul, blank=True, related_name="exam_syllabuses", verbose_name="Wymagane tule")
    strength_tests = models.JSONField(default=list, verbose_name="Testy siłowe")
    theory_qs = models.JSONField(default=list, verbose_name="Pytania teoretyczne")
    version = models.CharField(max_length=20, default="1.0.0")
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    is_draft = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"belt {self.belt}"

# Create your models here.
