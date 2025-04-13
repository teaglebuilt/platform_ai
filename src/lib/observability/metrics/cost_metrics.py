import logging
import asyncio
from typing import Optional
from datetime import datetime

from lib.clients.openai_api_client import OpenAIClient

from prometheus_client import Gauge, Counter, Histogram


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CostMetrics:
    def __init__(self):
        self.usage_total = Gauge(
            'openai_usage_total_usd',
            'Total amount spent on OpenAI project in USD',
            ['project_id', 'time_period']
        )

        self.usage_by_model = Gauge(
            'openai_usage_by_model_usd',
            'Amount spent by model in USD',
            ['project_id', 'model', 'operation']
        )

        self.api_requests = Counter(
            'openai_api_requests_total',
            'Total number of API requests',
            ['project_id', 'model', 'operation', 'status_code']
        )

        self.tokens_used = Counter(
            'openai_tokens_used_total',
            'Total tokens used',
            ['project_id', 'model', 'token_type']
        )

        self.cost_rate = Histogram(
            'openai_cost_rate_usd',
            'Cost rate distribution in USD',
            ['project_id', 'model'],
            buckets=[0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
        )

        self.pricing_info = Gauge(
            'openai_model_pricing_usd_per_1k',
            'Current pricing for models in USD per 1k tokens',
            ['model', 'token_type']
        )


class MetricsUpdater:
    def __init__(self, config: dict, metrics: CostMetrics, client: OpenAIClient):
        self.config = config
        self.metrics = metrics
        self.client = client

    async def update_pricing_metrics(self):
        """Update metrics with current pricing information"""
        pricing = await self.client.get_model_pricing()
        for model, prices in pricing.items():
            for token_type, price in prices.items():
                self.metrics.pricing_info.labels(
                    model=model,
                    token_type=token_type
                ).set(price)

    async def calculate_cost(self, usage_record: dict) -> Optional[dict]:
        """Calculate cost for a single usage record"""
        model = usage_record.get('snapshot_id', 'unknown')
        operation = usage_record.get('operation', 'unknown')
        token_type = None

        if operation in ['completion', 'embedding']:
            token_type = 'completion'
        elif operation == 'prompt':
            token_type = 'prompt'

        pricing = await self.client.get_model_pricing()
        model_pricing = pricing.get(model, {})
        price_per_1k = model_pricing.get(operation if operation in ['embedding'] else token_type, 0)
        price_per_token = price_per_1k / 1000

        prompt_tokens = usage_record.get('n_context_tokens_total', 0)
        completion_tokens = usage_record.get('n_generated_tokens_total', 0)
        total_tokens = prompt_tokens + completion_tokens

        cost = total_tokens * price_per_token

        return {
            'model': model,
            'operation': operation,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'cost': cost,
            'price_per_1k': price_per_1k
        }

    async def update_metrics(self):
        """Update all Prometheus metrics with current OpenAI usage data"""
        try:
            await self.update_pricing_metrics()

            today = datetime.now().date()
            first_day_of_month = today.replace(day=1)
            date_format = "%Y-%m-%d"

            # Fetch usage data concurrently
            monthly_usage, daily_usage = await asyncio.gather(
                self.client.get_usage(
                    first_day_of_month.strftime(date_format),
                    today.strftime(date_format)
                ),
                self.client.get_usage(
                    today.strftime(date_format),
                    today.strftime(date_format)
                )
            )

            # Process usage data
            monthly_total = 0.0
            model_breakdown = {}

            for record in monthly_usage:
                cost_data = await self.calculate_cost(record)
                if not cost_data:
                    continue

                monthly_total += cost_data['cost']

                # Aggregate by model and operation
                key = (cost_data['model'], cost_data['operation'])
                model_breakdown[key] = model_breakdown.get(key, 0) + cost_data['cost']

                # Update token counters
                self.metrics.tokens_used.labels(
                    project_id='default',
                    model=cost_data['model'],
                    token_type='prompt'
                ).inc(cost_data['prompt_tokens'])

                self.metrics.tokens_used.labels(
                    project_id='default',
                    model=cost_data['model'],
                    token_type='completion'
                ).inc(cost_data['completion_tokens'])

                # Record cost rate
                self.metrics.cost_rate.labels(
                    project_id='default',
                    model=cost_data['model']
                ).observe(cost_data['cost'])

            # Set monthly total
            self.metrics.usage_total.labels(
                project_id='default',
                time_period='current_month'
            ).set(monthly_total)

            # Set model breakdowns
            for (model, operation), cost in model_breakdown.items():
                self.metrics.usage_by_model.labels(
                    project_id='default',
                    model=model,
                    operation=operation
                ).set(cost)

            # Process daily data
            daily_costs = []
            for record in daily_usage:
                cost_data = await self.calculate_cost(record)
                if cost_data:
                    daily_costs.append(cost_data['cost'])

            daily_total = sum(daily_costs)
            self.metrics.usage_total.labels(
                project_id='default',
                time_period='current_day'
            ).set(daily_total)

            logger.info(f"Metrics updated - Monthly: ${monthly_total:.2f}, Daily: ${daily_total:.2f}")

        except Exception as e:
            logger.error(f"Error updating metrics: {e}", exc_info=True)
