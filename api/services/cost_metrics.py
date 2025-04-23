import os
import asyncio
from datetime import datetime, timezone, timedelta, date

import requests
from prometheus_client import CollectorRegistry, Gauge, make_asgi_app

registry = CollectorRegistry()

daily_cost_gauge = Gauge("openai_daily_cost_usd", "OpenAI daily usage cost in USD", registry=registry)
monthly_cost_gauge = Gauge("openai_monthly_cost_usd", "OpenAI monthly usage cost in USD", registry=registry)
total_requests_gauge = Gauge("openai_daily_requests_total", "Total OpenAI requests for the day", registry=registry)
input_tokens_gauge = Gauge("openai_daily_input_tokens", "Total OpenAI input tokens for the day", registry=registry)
output_tokens_gauge = Gauge("openai_daily_output_tokens", "Total OpenAI output tokens for the day", registry=registry)


def get_headers():
    return {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "OpenAI-Organization": f"{os.getenv('OPENAI_ORGANIZATION_ID')}",
        "OpenAI-Project": f"{os.getenv('OPENAI_PROJECT_ID')}",
        "Content-Type": "application/json",
    }


def fetch_usage():
    usage_url = "https://api.openai.com/v1/organization/usage/completions"
    start_time = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
    params = {
        "start_time": start_time,
        "bucket_width": "1d",
        "limit": 30
    }
    response = requests.get(usage_url, headers=get_headers(), params=params)
    return response.json().get("data", []) if response.ok else []


def fetch_costs():
    cost_url = "https://api.openai.com/v1/organization/costs"
    start_time = int((datetime.now(timezone.utc) - timedelta(days=30)).timestamp())
    params = {
        "start_time": start_time,
        "bucket_width": "1d",
        "limit": 30
    }
    response = requests.get(cost_url, headers=get_headers(), params=params)
    return response.json().get("data", []) if response.ok else []


def update_metrics():
    usage_data = fetch_usage()
    cost_data = fetch_costs()
    today = date.today()
    monthly_cost = 0.0
    daily_cost = 0.0
    input_tokens = 0
    output_tokens = 0
    total_requests = 0

    for bucket in cost_data:
        bucket_date = datetime.fromtimestamp(bucket["start_time"], timezone.utc).date()
        value = sum(r.get("amount", {}).get("value", 0) for r in bucket.get("results", []))
        if bucket_date.month == today.month and bucket_date.year == today.year:
            monthly_cost += value
            if bucket_date == today:
                daily_cost += value

    for bucket in usage_data:
        bucket_date = datetime.fromtimestamp(bucket["start_time"], timezone.utc).date()
        for result in bucket.get("results", []):
            if bucket_date == today:
                input_tokens += result.get("input_tokens", 0)
                output_tokens += result.get("output_tokens", 0)
                total_requests += result.get("num_model_requests", 0)

    daily_cost_gauge.set(round(daily_cost, 4))
    monthly_cost_gauge.set(round(monthly_cost, 4))
    input_tokens_gauge.set(input_tokens)
    output_tokens_gauge.set(output_tokens)
    total_requests_gauge.set(total_requests)


async def metric_scheduler():
    while True:
        update_metrics()
        await asyncio.sleep(3600)


metrics_app = make_asgi_app(registry=registry)
