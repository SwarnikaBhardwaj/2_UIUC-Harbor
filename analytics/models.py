from django.db import models
from django.utils import timezone


class AnalyticsEvent(models.Model):
    """
    Lightweight event log for dashboard analytics.

    This is intentionally minimal and JSON-friendly so the dashboard can compute:
    performance, behavior, and cost metrics from a single table.
    """

    FEATURE_CHOICES = [
        ("ai_description", "AI Description"),
        ("manual_entry", "Manual Entry"),
    ]

    MODEL_CHOICES = [
        ("local_flan", "Local FLAN"),
        ("gemini_fallback", "External Fallback"),
    ]

    LISTING_TYPE_CHOICES = [
        ("SERVICE", "Service"),
        ("FUNDRAISER", "Fundraiser"),
        ("SELLER", "Seller"),
    ]

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)

    feature = models.CharField(max_length=32, choices=FEATURE_CHOICES)
    model = models.CharField(max_length=32, choices=MODEL_CHOICES)
    used_fallback = models.BooleanField(default=False)

    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES, blank=True, default="")
    query_length = models.PositiveIntegerField(null=True, blank=True)
    converted = models.BooleanField(default=False)

    latency_ms = models.FloatField()
    cost_usd = models.FloatField(default=0.0)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"AnalyticsEvent({self.timestamp.isoformat()}, {self.feature}, {self.model})"

