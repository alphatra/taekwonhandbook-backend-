from django.db import models
from tkh_lexicon.models import Technique
from tkh_patterns.models import Tul


class MediaAsset(models.Model):
    KIND_CHOICES = (
        ("video", "Video"),
        ("image", "Image"),
        ("audio", "Audio"),
    )
    STATUS_CHOICES = (
        ("uploaded", "Uploaded"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
    )

    file = models.CharField(max_length=512)  # key/path in bucket
    kind = models.CharField(max_length=16, choices=KIND_CHOICES)
    codec = models.CharField(max_length=64, blank=True, null=True)
    resolutions = models.JSONField(default=list)
    duration = models.FloatField(default=0.0)
    thumbnails = models.JSONField(default=list)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="uploaded")
    meta = models.JSONField(default=dict, blank=True)
    techniques = models.ManyToManyField(Technique, blank=True, related_name="media_assets", verbose_name="Powiązane techniki")
    tuls = models.ManyToManyField(Tul, blank=True, related_name="media_assets", verbose_name="Powiązane tule")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.kind}:{self.file} ({self.status})"

# Create your models here.
