import os
from typing import Optional
from datetime import datetime
from lib.observability.logging import get_logger
import aiohttp

logger = get_logger()

class OpenAIAPIConfig:
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_ORGANIZATION: Optional[str] = os.getenv('OPENAI_ORGANIZATION')
    PRICING_REFRESH_INTERVAL: int = 86400 # daily


class OpenAIClient:
    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, config: OpenAIAPIConfig):
        self.config = config
        self.session = aiohttp.ClientSession()
        self._model_pricing: dict[str, dict[str, float]] = {}
        self._last_pricing_update: Optional[datetime] = None

    async def close(self):
        await self.session.close()

    async def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> tuple[Optional[dict], int]:
        headers = {
            "Authorization": f"Bearer {self.config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        if self.config.OPENAI_ORGANIZATION:
            headers["OpenAI-Organization"] = self.config.OPENAI_ORGANIZATION

        url = f"{self.BASE_URL}/{endpoint}"

        try:
            async with self.session.request(
                method,
                url,
                headers=headers,
                **kwargs
            ) as response:
                data = await response.json() if response.status != 204 else None
                return data, response.status
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None, 500

    async def get_usage(self, start_date: str, end_date: str) -> list[dict]:
        """Fetch usage data from OpenAI API"""
        endpoint = f"usage?date={start_date}"
        if start_date != end_date:
            endpoint += f"&end_date={end_date}"

        data, status = await self._make_request(endpoint)
        if status == 200:
            return data.get('data', [])
        logger.error(f"Failed to fetch usage data: {status}")
        return []

    async def get_model_pricing(self) -> dict[str, dict[str, float]]:
        """Fetch current model pricing from OpenAI"""
        if (self._last_pricing_update and
            (datetime.now() - self._last_pricing_update).total_seconds() < self.config.PRICING_REFRESH_INTERVAL):
            return self._model_pricing

        logger.info("Refreshing model pricing information")

        default_pricing = {
            'gpt-4': {
                'prompt': 0.03,
                'completion': 0.06,
            },
            'gpt-4-32k': {
                'prompt': 0.06,
                'completion': 0.12,
            },
            'gpt-3.5-turbo': {
                'prompt': 0.0015,
                'completion': 0.002,
            },
            'text-embedding-ada-002': {
                'embedding': 0.0001,
            }
        }

        try:
            # This is a placeholder - replace with actual API call if available
            # For now, we'll use the defaults but log that we tried
            logger.warning("OpenAI pricing API not officially available - using default pricing")
            self._model_pricing = default_pricing
            self._last_pricing_update = datetime.now()
            return self._model_pricing
        except Exception as e:
            logger.error(f"Failed to fetch pricing: {e}. Using defaults")
            return default_pricing
