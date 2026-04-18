(function () {
    "use strict";

    const LABEL_MAP = {
        ai_description: "AI Description",
        manual_entry: "Manual Entry",
        local_flan: "Local FLAN",
        // Backend may still emit the key "gemini_fallback"; keep the UI label generic.
        gemini_fallback: "External Fallback",
    };

    const COLOR_TOKENS = {
        brand: "#1f4f95",
        brandSoft: "rgba(31, 79, 149, 0.18)",
        accent: "#0f766e",
        accentSoft: "rgba(15, 118, 110, 0.18)",
        neutral: "#64748b",
        neutralSoft: "rgba(100, 116, 139, 0.2)",
        chartPalette: ["#1f4f95", "#0f766e", "#d97706", "#0369a1", "#2f855a", "#4b5563"],
    };

    document.addEventListener("DOMContentLoaded", initDashboard);

    function initDashboard() {
        (async () => {
            const apiData = await fetchDashboardData();
            const payload = apiData || readEmbeddedDashboardData();

            const summary = asObject(payload.summary);
            const avgQueryLength = toNumber(payload.avg_query_length);
            const conversionRate = toNumber(payload.conversion_rate);

            renderKpis(summary, avgQueryLength, conversionRate);

            if (typeof window.Chart === "undefined") {
                showAllChartErrors("Chart library failed to load.");
                return;
            }

            applyChartDefaults();
            renderRequiredCharts(payload);
        })();
    }

    async function fetchDashboardData() {
        try {
            const response = await fetch("/api/dashboard-data/", {
                method: "GET",
                headers: { Accept: "application/json" },
                credentials: "same-origin",
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const contentType = response.headers.get("content-type") || "";
            if (!contentType.includes("application/json")) {
                throw new Error("Non-JSON response");
            }

            return await response.json();
        } catch (error) {
            console.warn("Dashboard data fetch failed; falling back to embedded context.", error);
            return null;
        }
    }

    function readEmbeddedDashboardData() {
        return {
            summary: readJSONScript("summary-data", {}),
            avg_query_length: readJSONScript("avg-query-length-data", null),
            conversion_rate: readJSONScript("conversion-rate-data", null),
            latency_over_time: readJSONScript("latency-over-time-data", []),
            feature_usage: readJSONScript("feature-usage-data", []),
            listing_type_counts: readJSONScript("listing-type-counts-data", []),
            avg_latency_by_listing_type: readJSONScript("avg-latency-by-listing-type-data", []),
            cost_over_time: readJSONScript("cost-over-time-data", []),
            model_usage_split: readJSONScript("model-usage-split-data", []),
        };
    }

    function renderRequiredCharts(payload) {
        const latencyOverTime = normalizeSeries(
            payload.latency_over_time,
            ["day", "date", "timestamp", "label", "x"],
            ["avg_latency", "latency", "value", "y"]
        );

        const featureUsage = normalizeCategoryCounts(
            payload.feature_usage,
            ["feature", "name", "label", "type", "source"],
            ["count", "total", "value", "requests"]
        );

        const costOverTime = normalizeSeries(
            payload.cost_over_time,
            ["day", "date", "timestamp", "label", "x"],
            ["total_cost", "cost", "value", "y"]
        );

        const listingTypeCounts = normalizeCategoryCounts(
            payload.listing_type_counts,
            ["listing_type", "type", "name", "label", "category"],
            ["count", "total", "value"]
        );

        const avgLatencyByListingType = normalizeCategoryCounts(
            payload.avg_latency_by_listing_type,
            ["listing_type", "type", "name", "label", "category"],
            ["avg_latency", "latency", "value"]
        );

        const modelUsageSplit = normalizeCategoryCounts(
            payload.model_usage_split,
            ["model", "name", "label", "type", "source"],
            ["count", "total", "value", "requests"]
        );

        renderLineChart({
            canvasId: "latency-over-time-chart",
            emptyId: "latency-over-time-empty",
            points: latencyOverTime,
            title: "Latency Over Time",
            xLabel: "Day",
            yLabel: "Average Latency (ms)",
            color: COLOR_TOKENS.brand,
            backgroundColor: COLOR_TOKENS.brandSoft,
        });

        renderDonutChart({
            canvasId: "feature-usage-chart",
            emptyId: "feature-usage-empty",
            values: featureUsage,
            title: "Feature Usage",
        });

        renderLineChart({
            canvasId: "cost-over-time-chart",
            emptyId: "cost-over-time-empty",
            points: costOverTime,
            title: "Cost Over Time",
            xLabel: "Day",
            yLabel: "Total Cost ($)",
            color: COLOR_TOKENS.accent,
            backgroundColor: COLOR_TOKENS.accentSoft,
        });

        renderBarChart({
            canvasId: "listing-type-counts-chart",
            emptyId: "listing-type-counts-empty",
            values: listingTypeCounts,
            title: "Listing Type Counts",
            xLabel: "Listing Type",
            yLabel: "Count",
            color: COLOR_TOKENS.brand,
        });

        renderBarChart({
            canvasId: "avg-latency-by-listing-type-chart",
            emptyId: "avg-latency-by-listing-type-empty",
            values: avgLatencyByListingType,
            title: "Average Latency by Listing Type",
            xLabel: "Listing Type",
            yLabel: "Average Latency (ms)",
            color: COLOR_TOKENS.neutral,
        });

        renderDonutChart({
            canvasId: "model-usage-split-chart",
            emptyId: "model-usage-split-empty",
            values: modelUsageSplit,
            title: "Model Usage Split",
        });
    }

    function renderKpis(summary, avgQueryLength, conversionRate) {
        setText("kpi-total-requests", formatInteger(summary.total_requests));
        setText("kpi-avg-latency", formatDecimal(summary.avg_latency, 2));
        setText("kpi-fallback-rate", formatPercent(summary.fallback_rate));
        setText("kpi-avg-cost", formatCurrency(summary.avg_cost));
        setText("kpi-total-cost", formatCurrency(summary.total_cost));
        setText("kpi-unique-users", formatInteger(summary.unique_users));
        setText("kpi-avg-query-length", formatDecimal(avgQueryLength, 2));
        setText("kpi-conversion-rate", formatPercent(conversionRate));
    }

    function renderLineChart(config) {
        const labels = config.points.map((point) => point.label);
        const values = config.points.map((point) => point.value);

        if (!labels.length || !values.length) {
            showEmptyState(config.canvasId, config.emptyId);
            return;
        }

        hideEmptyState(config.canvasId, config.emptyId);
        const context = getChartContext(config.canvasId);
        if (!context) {
            return;
        }

        new Chart(context, {
            type: "line",
            data: {
                labels,
                datasets: [
                    {
                        label: config.title,
                        data: values,
                        borderColor: config.color,
                        backgroundColor: config.backgroundColor,
                        borderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 4,
                        fill: true,
                        tension: 0.25,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: config.title,
                        color: "#12233d",
                        font: { family: "Syne", size: 13, weight: "700" },
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: config.xLabel,
                        },
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: config.yLabel,
                        },
                    },
                },
            },
        });
    }

    function renderBarChart(config) {
        const labels = config.values.map((item) => item.label);
        const values = config.values.map((item) => item.value);

        if (!labels.length || !values.length) {
            showEmptyState(config.canvasId, config.emptyId);
            return;
        }

        hideEmptyState(config.canvasId, config.emptyId);
        const context = getChartContext(config.canvasId);
        if (!context) {
            return;
        }

        new Chart(context, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    {
                        label: config.title,
                        data: values,
                        backgroundColor: config.color,
                        borderRadius: 8,
                        maxBarThickness: 48,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: config.title,
                        color: "#12233d",
                        font: { family: "Syne", size: 13, weight: "700" },
                    },
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: config.xLabel,
                        },
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: config.yLabel,
                        },
                    },
                },
            },
        });
    }

    function renderDonutChart(config) {
        const labels = config.values.map((item) => item.label);
        const values = config.values.map((item) => item.value);

        if (!labels.length || !values.length) {
            showEmptyState(config.canvasId, config.emptyId);
            return;
        }

        hideEmptyState(config.canvasId, config.emptyId);
        const context = getChartContext(config.canvasId);
        if (!context) {
            return;
        }

        const colors = labels.map((_, index) => COLOR_TOKENS.chartPalette[index % COLOR_TOKENS.chartPalette.length]);

        new Chart(context, {
            type: "doughnut",
            data: {
                labels,
                datasets: [
                    {
                        data: values,
                        backgroundColor: colors,
                        borderColor: "#ffffff",
                        borderWidth: 2,
                        hoverOffset: 4,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
                cutout: "60%",
                plugins: {
                    title: {
                        display: true,
                        text: config.title,
                        color: "#12233d",
                        font: { family: "Syne", size: 13, weight: "700" },
                    },
                    legend: {
                        position: "bottom",
                    },
                },
            },
        });
    }

    function normalizeSeries(raw, xKeys, yKeys) {
        // Accept both list-of-objects and object-map payloads from backend serializers.
        const parsed = ensureParsed(raw);
        if (!parsed) {
            return [];
        }

        if (Array.isArray(parsed)) {
            return parsed
                .map((item, index) => {
                    if (item && typeof item === "object" && !Array.isArray(item)) {
                        const label = readByKeys(item, xKeys);
                        const value = toNumber(readByKeys(item, yKeys));
                        return buildPoint(label, value);
                    }

                    if (Array.isArray(item) && item.length >= 2) {
                        return buildPoint(item[0], toNumber(item[1]));
                    }

                    const numeric = toNumber(item);
                    return buildPoint(index + 1, numeric);
                })
                .filter(Boolean);
        }

        if (typeof parsed === "object") {
            return Object.entries(parsed)
                .map(([label, value]) => buildPoint(label, toNumber(value)))
                .filter(Boolean);
        }

        return [];
    }

    function normalizeCategoryCounts(raw, labelKeys, valueKeys) {
        // Some backends emit {"label": count}, while others emit [{"label": "...", "count": n}].
        const parsed = ensureParsed(raw);
        if (!parsed) {
            return [];
        }

        if (Array.isArray(parsed)) {
            return parsed
                .map((item, index) => {
                    if (item && typeof item === "object" && !Array.isArray(item)) {
                        const label = readByKeys(item, labelKeys);
                        const value = toNumber(readByKeys(item, valueKeys));
                        return buildCategoryPoint(label, value);
                    }

                    if (Array.isArray(item) && item.length >= 2) {
                        return buildCategoryPoint(item[0], toNumber(item[1]));
                    }

                    const numeric = toNumber(item);
                    return buildCategoryPoint(`Item ${index + 1}`, numeric);
                })
                .filter(Boolean);
        }

        if (typeof parsed === "object") {
            return Object.entries(parsed)
                .map(([label, value]) => buildCategoryPoint(label, toNumber(value)))
                .filter(Boolean);
        }

        return [];
    }

    function buildPoint(label, value) {
        if (value === null || !Number.isFinite(value)) {
            return null;
        }

        return {
            label: prettyLabel(label),
            value,
        };
    }

    function buildCategoryPoint(label, value) {
        if (value === null || !Number.isFinite(value)) {
            return null;
        }

        return {
            label: prettyLabel(label),
            value,
        };
    }

    function prettyLabel(rawLabel) {
        const token = String(rawLabel ?? "").trim();
        if (!token) {
            return "Unknown";
        }

        if (Object.prototype.hasOwnProperty.call(LABEL_MAP, token)) {
            return LABEL_MAP[token];
        }

        return token
            .replace(/[_-]+/g, " ")
            .replace(/\s+/g, " ")
            .trim()
            .replace(/\b\w/g, (char) => char.toUpperCase());
    }

    function readJSONScript(id, fallbackValue) {
        const scriptNode = document.getElementById(id);
        if (!scriptNode) {
            return fallbackValue;
        }

        const rawText = scriptNode.textContent ? scriptNode.textContent.trim() : "";
        if (!rawText) {
            return fallbackValue;
        }

        try {
            return JSON.parse(rawText);
        } catch (error) {
            console.error(`Failed to parse JSON data from #${id}`, error);
            return fallbackValue;
        }
    }

    function ensureParsed(value) {
        if (value === null || value === undefined) {
            return null;
        }

        if (typeof value === "string") {
            // Handles JSON that was already serialized before being passed to json_script.
            const trimmed = value.trim();
            if (!trimmed) {
                return null;
            }

            try {
                return JSON.parse(trimmed);
            } catch (_error) {
                return value;
            }
        }

        return value;
    }

    function asObject(value) {
        const parsed = ensureParsed(value);
        if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
            return parsed;
        }
        return {};
    }

    function readByKeys(objectValue, keys) {
        for (const key of keys) {
            if (Object.prototype.hasOwnProperty.call(objectValue, key) && objectValue[key] !== null && objectValue[key] !== undefined) {
                return objectValue[key];
            }
        }
        return null;
    }

    function getChartContext(canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            return null;
        }
        return canvas.getContext("2d");
    }

    function showEmptyState(canvasId, emptyId, message) {
        const canvas = document.getElementById(canvasId);
        const empty = document.getElementById(emptyId);

        if (canvas) {
            canvas.style.display = "none";
        }

        if (empty) {
            if (message) {
                empty.textContent = message;
            }
            empty.classList.add("is-visible");
        }
    }

    function hideEmptyState(canvasId, emptyId) {
        const canvas = document.getElementById(canvasId);
        const empty = document.getElementById(emptyId);

        if (canvas) {
            canvas.style.display = "block";
        }

        if (empty) {
            empty.classList.remove("is-visible");
        }
    }

    function showAllChartErrors(message) {
        const chartIds = [
            ["latency-over-time-chart", "latency-over-time-empty"],
            ["feature-usage-chart", "feature-usage-empty"],
            ["cost-over-time-chart", "cost-over-time-empty"],
            ["listing-type-counts-chart", "listing-type-counts-empty"],
            ["avg-latency-by-listing-type-chart", "avg-latency-by-listing-type-empty"],
            ["model-usage-split-chart", "model-usage-split-empty"],
        ];

        chartIds.forEach(([canvasId, emptyId]) => showEmptyState(canvasId, emptyId, message));
    }

    function setText(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = value;
        }
    }

    function toNumber(value) {
        if (value === null || value === undefined || value === "") {
            return null;
        }
        const numeric = Number(value);
        return Number.isFinite(numeric) ? numeric : null;
    }

    function formatInteger(value) {
        const numeric = toNumber(value);
        if (numeric === null) {
            return "--";
        }

        return new Intl.NumberFormat(undefined, {
            maximumFractionDigits: 0,
        }).format(numeric);
    }

    function formatDecimal(value, precision) {
        const numeric = toNumber(value);
        if (numeric === null) {
            return "--";
        }

        return new Intl.NumberFormat(undefined, {
            minimumFractionDigits: 0,
            maximumFractionDigits: precision,
        }).format(numeric);
    }

    function formatCurrency(value) {
        const numeric = toNumber(value);
        if (numeric === null) {
            return "--";
        }

        return new Intl.NumberFormat(undefined, {
            style: "currency",
            currency: "USD",
            minimumFractionDigits: 2,
            maximumFractionDigits: 4,
        }).format(numeric);
    }

    function formatPercent(value) {
        const numeric = toNumber(value);
        if (numeric === null) {
            return "--";
        }

        const adjusted = Math.abs(numeric) <= 1 ? numeric * 100 : numeric;
        return `${formatDecimal(adjusted, 2)}%`;
    }

    function applyChartDefaults() {
        Chart.defaults.font.family = '"DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
        Chart.defaults.font.size = 12;
        Chart.defaults.color = "#52647f";
        Chart.defaults.borderColor = "rgba(15, 23, 42, 0.12)";
        Chart.defaults.plugins.legend.labels.usePointStyle = true;
        Chart.defaults.plugins.legend.labels.boxWidth = 10;
    }
})();
