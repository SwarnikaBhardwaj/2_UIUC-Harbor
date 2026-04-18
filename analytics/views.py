from __future__ import annotations

import json
from typing import Any

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .services import (
    get_avg_latency_by_listing_type,
    get_avg_query_length,
    get_conversion_rate,
    get_cost_over_time,
    get_feature_usage,
    get_latency_over_time,
    get_listing_type_counts,
    get_model_usage_split,
    get_summary_metrics,
)


def _build_dashboard_data() -> dict[str, Any]:
    return {
        "summary": get_summary_metrics(),
        "avg_query_length": get_avg_query_length(),
        "conversion_rate": get_conversion_rate(),
        "latency_over_time": get_latency_over_time(),
        "feature_usage": get_feature_usage(),
        "listing_type_counts": get_listing_type_counts(),
        "avg_latency_by_listing_type": get_avg_latency_by_listing_type(),
        "cost_over_time": get_cost_over_time(),
        "model_usage_split": get_model_usage_split(),
    }


def _build_template_context() -> dict[str, Any]:
    data = _build_dashboard_data()

    return {
        "summary": data["summary"],
        "avg_query_length": data["avg_query_length"],
        "conversion_rate": data["conversion_rate"],
        "latency_over_time": json.dumps(data["latency_over_time"]),
        "feature_usage": json.dumps(data["feature_usage"]),
        "listing_type_counts": json.dumps(data["listing_type_counts"]),
        "avg_latency_by_listing_type": json.dumps(data["avg_latency_by_listing_type"]),
        "cost_over_time": json.dumps(data["cost_over_time"]),
        "model_usage_split": json.dumps(data["model_usage_split"]),
        "summary_json": json.dumps(data["summary"]),
    }


@require_GET
def dashboard_view(request):
    context = _build_template_context()
    return render(request, "analytics/dashboard.html", context)


@require_GET
def dashboard_data_api(request):
    data = _build_dashboard_data()
    return JsonResponse(data, json_dumps_params={"default": str})