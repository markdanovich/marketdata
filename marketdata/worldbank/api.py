from typing import Dict, List, Optional, Type, Union
import pandas as pd
from marketdata.base_api import BaseAPI
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)


class WorldBank(BaseAPI):
    def __init__(self, version: str = "2"):
        """
        WorldBank Indicators API wrapper
        """
        base_path = f"http://api.worldbank.org/v{version}/country"
        super().__init__(base_path)

    def get_data(
        self, indicator: str, date: str, country: Optional[str] = "all"
    ) -> Union[pd.DataFrame, None]:
        """
        Get data for indicator and countries for given date

        :param inidicator: the indicator code for the requested data
        :param date: date or date range e.g. single year "2000", year range "1980:2000", year and month range "2010M01:2013:M08"
        :param country: country for which to get the data. Country given by 3 letter code, can be multiple countries separated by ';' or 'all'.
        """

        url = f"{self.base_path}/{country}/indicator/{indicator}?date={date}&per_page=50&format=json"

        # The response is split into multiple pages, with a number of results per page.
        # get number of pages
        response = self._query(url)

        if response:
            # check that the response is a List
            if isinstance(response, List):
                # read in first page into dataframe
                df_response = pd.DataFrame(response[1])
            else:
                logger.error("Response has unexpected format")
                return None

            df = WorldBank._format_dataframe(df_response)

            try:
                num_pages = int(response[0]["pages"])
            except ValueError:
                logger.error("Got a non-integer number of pages")
                return None

            # there is only one page return the dataframe
            if num_pages == 1:
                return df

            # loop over the pages
            for page in range(2, num_pages + 1):
                # modify the url to retrieve the next page
                url_page = url + f"&page={page}"
                response_page = self._query(url_page)

                # check that the response is a List
                if isinstance(response_page, List):
                    df_response = pd.DataFrame(response_page[1])
                else:
                    logger.error("Response has unexpected format")
                    return None

                df_page = WorldBank._format_dataframe(df_response)

                # combine new page into previous dataframe
                df = pd.concat([df, df_page], axis=0)

            return df

        else:
            return None

    def get_countries(self):
        """
        Get a list of all coutries and metadata
        """
        url = f"{self.base_path}?format=json"
        response = self._query(url)

        if response:
            return pd.DataFrame(response[1])
        else:
            logger.warning("Response is empty")
            return None

    @staticmethod
    def _format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Helper to convert the json response fields for indicator and country which
        are provided as dictionary with id and value fields.

        :param df: the dataframe ontained from the raw json response.
        """
        df["indicator"] = df["indicator"].map(lambda x: x["value"])
        df["country"] = df["country"].map(lambda x: x["value"])
        return df
