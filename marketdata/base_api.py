import logging
from typing import Any, Dict, List, Optional, Union

import requests

logger = logging.getLogger(__name__)


class BaseAPI:
    def __init__(self, base_path: str, api_token: Optional[str] = None):
        self.base_path = base_path
        self.api_token = api_token

    def _query(self, url: str) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()
            except Exception:
                logger.error("Failed to read json response")
        else:
            logger.warning(f"Request failed with code: {response.status_code}")

        return None
