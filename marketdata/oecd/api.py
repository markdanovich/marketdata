from typing import Dict, List, Optional, Type, Union
import pandas as pd
from marketdata.base_api import BaseAPI
import logging

logger = logging.getLogger(__name__)


class OECD(BaseAPI):
    def __init__(self):
        """
        OECD API wrapper
        
        https://stats.oecd.org/index.aspx?queryid=86
        """
        base_path = "http://stats.oecd.org/SDMX-JSON/data"

        super().__init__(base_path)

    def get_data(
        self,
        dataset_id: str,
        filter_expression: str,
        from_date: str,
        to_date: str,
    ) -> pd.DataFrame:
        """
        Get data for series in a CSV format read into a pandas dataframe
        :param dataset_id: main identifier of dataset which contains indicators
        :filter_expression: expression to filter specific identifiers, countries and frequencies with + and . notation
        :from_date: start date, can be year, or year-month, year-quarter
        :to_date: end date, can be year, or year-month, year-quarter
        """

        url = f"{self.base_path}/{dataset_id}/{filter_expression}/all?startPeriod={from_date}&endPeriod={to_date}&dimensionAtObservation=allDimensions&contentType=csv"

        df = pd.read_csv(url)

        return df
