from typing import Optional
import pandas as pd
from marketdata.base_api import BaseAPI
from collections import OrderedDict
from pyjstat import pyjstat

class Eurostat(BaseAPI):
    def __init__(self, version: str = "2.1"):
        """
        Eurostat api wrapper
        https://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/rest-request
        https://ec.europa.eu/eurostat/data/database
        """
        base_path = f"http://ec.europa.eu/eurostat/wdds/rest/data/v{version}/json/en"
        super().__init__(base_path)

    def get_data(
        self, dataset_code: str, additional_filters: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get data from dataset
        :param dataset_code: code of the requeired dataset 
        """
        url = f"{self.base_path}/{dataset_code}"
        if additional_filters:
            url += f"?{additional_filters}"
        
        print(url)
        response = self._query(url)
        df = pyjstat.from_json_stat(response)[0]

        return df
