from datetime import timedelta

from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import AnalyticsEvent


def get_summary_metrics():
    qs = AnalyticsEvent.objects.all()

    total_requests = qs.count()
    avg_latency = qs.aggregate(avg_latency=Avg("latency_ms"))["avg_latency"] or 0
    avg_cost = qs.aggregate(avg_cost=Avg("cost_usd"))["avg_cost"] or 0
    total_cost = qs.aggregate(total_cost=Sum("cost_usd"))["total_cost"] or 0
    unique_users = qs.values("user_id").distinct().count()

    fallback_count = qs.filter(used_fallback=True).count()
    fallback_rate = (fallback_count / total_requests * 100) if total_requests > 0 else 0

    return {
        "total_requests": total_requests,
        "avg_latency": round(float(avg_latency), 2),
        "avg_cost": round(float(avg_cost), 4),
        "total_cost": round(float(total_cost), 4),
        "fallback_rate": round(fallback_rate, 2),
        "unique_users": unique_users,
    }


def get_latency_over_time(days=30):
    start_date = timezone.now() - timedelta(days=days)

    data = (
        AnalyticsEvent.objects
        .filter(timestamp__gte=start_date)
        .annotate(day=TruncDate("timestamp"))
        .values("day")
        .annotate(avg_latency=Avg("latency_ms"))
        .order_by("day")
    )

    return [
        {
            "day": item["day"].strftime("%Y-%m-%d"),
            "avg_latency": round(float(item["avg_latency"]), 2),
        }
        for item in data
    ]


def get_feature_usage():
    data = (
        AnalyticsEvent.objects
        .values("feature")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return list(data)


def get_listing_type_counts():
    data = (
        AnalyticsEvent.objects
        .values("listing_type")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return list(data)


def get_avg_latency_by_listing_type():
    data = (
        AnalyticsEvent.objects
        .values("listing_type")
        .annotate(avg_latency=Avg("latency_ms"))
        .order_by("-avg_latency")
    )

    return [
        {
            "listing_type": item["listing_type"],
            "avg_latency": round(float(item["avg_latency"]), 2),
        }
        for item in data
    ]


def get_cost_over_time(days=30):
    start_date = timezone.now() - timedelta(days=days)

    data = (
        AnalyticsEvent.objects
        .filter(timestamp__gte=start_date)
        .annotate(day=TruncDate("timestamp"))
        .values("day")
        .annotate(total_cost=Sum("cost_usd"))
        .order_by("day")
    )

    return [
        {
            "day": item["day"].strftime("%Y-%m-%d"),
            "total_cost": round(float(item["total_cost"] or 0), 4),
        }
        for item in data
    ]


def get_model_usage_split():
    data = (
        AnalyticsEvent.objects
        .values("model")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    return list(data)


def get_avg_query_length():
    value = AnalyticsEvent.objects.aggregate(avg_length=Avg("query_length"))["avg_length"] or 0
    return round(float(value), 2)


def get_conversion_rate():
    total_ai = AnalyticsEvent.objects.filter(feature="ai_description").count()
    converted_ai = AnalyticsEvent.objects.filter(
        feature="ai_description",
        converted=True,
    ).count()

    rate = (converted_ai / total_ai * 100) if total_ai > 0 else 0
    return round(rate, 2)