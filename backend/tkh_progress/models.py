from django.db import models
from django.conf import settings


class Progress(models.Model):
    ITEM_TYPES = (
        ("technique", "Technique"),
        ("tul", "Tul"),
        ("exercise", "Exercise"),
        ("plan", "Plan"),
        ("quiz", "Quiz"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=16, choices=ITEM_TYPES)
    item_id = models.IntegerField()
    status = models.CharField(max_length=24, default="seen")  # seen, in_progress, done
    score = models.FloatField(default=0.0)
    streaks = models.IntegerField(default=0)
    last_seen_at = models.DateTimeField(auto_now=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("user", "item_type", "item_id")
        indexes = [
            models.Index(fields=["user", "item_type", "item_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.item_type}:{self.item_id}"

# Create your models here.
