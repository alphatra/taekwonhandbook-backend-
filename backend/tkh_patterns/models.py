from django.db import models


class Tul(models.Model):
    name = models.CharField(max_length=64, db_index=True, verbose_name="Nazwa")
    belt = models.IntegerField(default=7, verbose_name="Pas")
    steps = models.JSONField(default=list, verbose_name="Kroki")
    diagram = models.URLField(blank=True, null=True, verbose_name="Diagram")
    tempo = models.JSONField(default=list, verbose_name="Tempo")
    videos = models.JSONField(default=dict, verbose_name="Wideo")
    meaning = models.TextField(blank=True, null=True, verbose_name="Znaczenie")
    judge_notes = models.TextField(blank=True, null=True, verbose_name="Uwagi sędziowskie")
    version = models.CharField(max_length=20, default="1.0.0", verbose_name="Wersja")
    valid_from = models.DateTimeField(auto_now_add=True, verbose_name="Ważne od")
    valid_to = models.DateTimeField(blank=True, null=True, verbose_name="Ważne do")
    is_draft = models.BooleanField(default=False, verbose_name="Szkic")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tul"
        verbose_name_plural = "Tule"
        ordering = ["belt", "name"]

    def __str__(self) -> str:
        return self.name

# Create your models here.
