from typing import Dict, List, Optional, Type, Union
import pandas as pd
from marketdata.base_api import BaseAPI
import logging

logger = logging.getLogger(__name__)


class Fred(BaseAPI):
    def __init__(self, api_token: str, version: str = "2"):
        """
        FRED API wrapper
        """
        base_path = f"https://api.stlouisfed.org/fred/series/observations"

        super().__init__(base_path, api_token)

    def get_data(
        self,
        series_id: str,
        from_date: str,
        to_date: str,
        frequency: str = "q",
        agg_method: str = "eop",
    ) -> Union[pd.DataFrame, None]:
        """
        Get data for series
        """

        url = f"{self.base_path}?series_id={series_id}&api_key={self.api_token}&file_type=json&observation_start={from_date}&observation_end={to_date}&frequency={frequency}&aggregation_method={agg_method}"

        resp = self._query(url)

        if isinstance(resp, dict):
            df = pd.DataFrame(resp["observations"])
            return df
        
        return None
