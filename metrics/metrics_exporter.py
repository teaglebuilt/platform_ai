import os
import asyncio

from prometheus_client import start_http_server

from lib.clients.openai_api_client import OpenAIClient, OpenAIAPIConfig
from lib.observability.metrics.cost_metrics import CostMetrics, MetricsUpdater
from lib.observability.logging import get_logger


logger = get_logger()


class ExporterConfig:
    SCRAPE_INTERVAL: int = int(os.getenv('SCRAPE_INTERVAL', '300')) # 5 minutes
    PRICING_REFRESH_INTERVAL: int = 86400
    EXPORTER_PORT: int = 9400

async def main():
    config = ExporterConfig()
    metrics = CostMetrics()
    client = OpenAIClient(OpenAIAPIConfig())
    updater = MetricsUpdater(config.__dict__, metrics, client)

    # Start metrics server
    start_http_server(config.EXPORTER_PORT)
    logger.info(f"Prometheus exporter started on port {config.EXPORTER_PORT}")

    try:
        while True:
            await updater.update_metrics()
            await asyncio.sleep(config.SCRAPE_INTERVAL)
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())
