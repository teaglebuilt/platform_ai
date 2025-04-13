import os
from typing import Optional


class Config:
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_ORGANIZATION: Optional[str] = os.getenv('OPENAI_ORGANIZATION')
    EXPORTER_PORT: int = int(os.getenv('EXPORTER_PORT', '8000'))
    SCRAPE_INTERVAL: int = int(os.getenv('SCRAPE_INTERVAL', '300')) # 5 minutes
    PRICING_REFRESH_INTERVAL: int = 86400 # daily
