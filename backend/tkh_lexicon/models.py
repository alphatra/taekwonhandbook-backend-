from django.db import models


class Technique(models.Model):
    names = models.JSONField(
        default=dict,
        verbose_name="Nazwy (PL/EN/KR)",
        help_text="Słownik nazw, np. {pl,en,kr}",
    )
    audio = models.URLField(blank=True, null=True, verbose_name="Audio (wymowa)")
    category = models.CharField(max_length=64, db_index=True, verbose_name="Kategoria")
    min_belt = models.IntegerField(
        default=10, verbose_name="Minimalny pas", help_text="10=9 kup ... 1=1 kup, 0=1 dan"
    )
    key_points = models.JSONField(default=list, verbose_name="Punkty kluczowe")
    common_mistakes = models.JSONField(default=list, verbose_name="Błędy częste")
    videos = models.JSONField(default=dict, verbose_name="Wideo", help_text="{front,side,slow}")
    safety = models.TextField(blank=True, null=True, verbose_name="Bezpieczeństwo")
    tags = models.JSONField(default=list, verbose_name="Tagi")
    version = models.CharField(max_length=20, default="1.0.0", verbose_name="Wersja")
    valid_from = models.DateTimeField(auto_now_add=True, verbose_name="Ważne od")
    valid_to = models.DateTimeField(blank=True, null=True, verbose_name="Ważne do")
    is_draft = models.BooleanField(default=False, verbose_name="Szkic (draft)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Technika"
        verbose_name_plural = "Techniki"
        indexes = [
            models.Index(fields=["category"]),
        ]
        ordering = ["id"]

    def __str__(self) -> str:
        return self.names.get("pl") or self.names.get("en") or f"Technique {self.pk}"


# Create your models here.
