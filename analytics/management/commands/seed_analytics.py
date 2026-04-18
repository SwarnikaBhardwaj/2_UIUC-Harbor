from __future__ import annotations

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from analytics.models import AnalyticsEvent


class Command(BaseCommand):
    help = "Seed AnalyticsEvent with realistic dummy data for the analytics dashboard."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="How many days of historical data to generate (default: 30).",
        )
        parser.add_argument(
            "--per-day",
            type=int,
            default=40,
            help="Approximate number of events per day (default: 40).",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing AnalyticsEvent rows before seeding.",
        )

    def handle(self, *args, **options):
        days = max(1, int(options["days"]))
        per_day = max(1, int(options["per_day"]))
        reset = bool(options["reset"])

        self._ensure_table_exists()

        if reset:
            deleted, _ = AnalyticsEvent.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing AnalyticsEvent rows.")

        rng = random.Random()
        now = timezone.now()

        user_pool = list(range(1, 61))  # lightweight "unique users" pool
        listing_type_weights = [0.6, 0.25, 0.15]

        to_create: list[AnalyticsEvent] = []

        for day_offset in range(days):
            day_start = (now - timedelta(days=day_offset)).replace(hour=0, minute=0, second=0, microsecond=0)
            day_volume = per_day + rng.randint(-(per_day // 4), per_day // 4)
            day_volume = max(0, day_volume)

            for _ in range(day_volume):
                timestamp = day_start + timedelta(seconds=rng.randint(0, 86399))

                feature = rng.choices(
                    population=["ai_description", "manual_entry"],
                    weights=[0.72, 0.28],
                    k=1,
                )[0]

                model = rng.choices(
                    population=["local_flan", "gemini_fallback"],
                    weights=[0.88, 0.12],
                    k=1,
                )[0]
                used_fallback = model == "gemini_fallback"

                listing_type = rng.choices(
                    population=["SERVICE", "FUNDRAISER", "SELLER"],
                    weights=listing_type_weights,
                    k=1,
                )[0]

                # Query length: AI usage tends to correlate with longer prompts.
                base_query_len = 135 if feature == "ai_description" else 75
                query_length = int(max(5, rng.gauss(base_query_len, 25)))

                # Latency and cost: fallback calls are slower and costlier.
                base_latency = 780 if not used_fallback else 2150
                latency_ms = float(max(120.0, rng.gauss(base_latency, 240 if not used_fallback else 520)))

                base_cost = 0.0003 if not used_fallback else 0.0046
                cost_usd = float(max(0.0, rng.gauss(base_cost, base_cost * 0.25)))

                conversion_prob = 0.18 if feature == "ai_description" else 0.09
                converted = rng.random() < conversion_prob

                user_id = rng.choice(user_pool) if rng.random() < 0.92 else None

                to_create.append(
                    AnalyticsEvent(
                        timestamp=timestamp,
                        user_id=user_id,
                        feature=feature,
                        model=model,
                        used_fallback=used_fallback,
                        listing_type=listing_type,
                        query_length=query_length,
                        converted=converted,
                        latency_ms=latency_ms,
                        cost_usd=cost_usd,
                    )
                )

        AnalyticsEvent.objects.bulk_create(to_create, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(to_create)} AnalyticsEvent rows."))

    def _ensure_table_exists(self) -> None:
        """
        Make the command work on a fresh DB even if migrations haven't been created/applied yet.
        """
        table_name = AnalyticsEvent._meta.db_table
        existing_tables = set(connection.introspection.table_names())
        if table_name in existing_tables:
            return

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(AnalyticsEvent)

