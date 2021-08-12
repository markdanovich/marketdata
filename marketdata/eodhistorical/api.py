import logging
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from pandas.core import api

from .definitions import EndPoint, Period
from marketdata.exceptions import DateRangeError
from marketdata.base_api import BaseAPI


logger = logging.getLogger(__name__)


class EODHistorical(BaseAPI):
    def __init__(
        self, api_token: Optional[str] = None, token_path: Optional[str] = None
    ):
        """
        EOD Historical Data API wrapper
        https://eodhistoricaldata.com/financial-apis/

        :param api_token: String token to access EOD API
        :param token_path: The path to the file containing the API token
        """

        if api_token:
            self.api_token = api_token
        elif token_path:
            with open(token_path, "r") as f:
                self.api_token = f.read().rstrip("\n")
        else:
            with open("./.eod_token", "r") as f:
                self.api_token = f.read().rstrip("\n")

        base_path = "https://eodhistoricaldata.com/api"

        super().__init__(base_path, api_token)

    def list_exchanges(self) -> pd.DataFrame:
        """
        Get available exchanges as a pandas dataframe
        """
        url = f"{self.base_path}/{EndPoint.EXCHANGES.value}/?api_token={self.api_token}&fmt=json"
        response = self._query(url)

        df_exchanges = pd.DataFrame(response)

        return df_exchanges

    def list_tickers(self, exchange_code: str) -> pd.DataFrame:
        """
        Get available tickers for exchange as a pandas dataframe

        :param exchange_code: code of the exchange
        """
        url = f"{self.base_path}/{EndPoint.LIST_OF_TICKERS.value}/{exchange_code}?api_token={self.api_token}&fmt=json"
        response = self._query(url)

        df_tickers = pd.DataFrame(response)

        return df_tickers

    def eod_data(
        self,
        exchange_code: str,
        symbol_code: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        period: Optional[str] = "d",
        order: Optional[str] = "a",
    ) -> pd.DataFrame:
        """
        Get end of day data for given symbol and dates

        :param exchange_code: the exchange code for the symbol
        :param symbol_code: the symbol code
        :period: The period of the data daily, weekly or monthly
        :from: the start date 'YYYY-MM-DD'
        :to: the end date 'YYYY-MM-DD'
        """

        # check period is valid
        periods = [p.value for p in Period]
        assert period in periods, f"Invalid period, period needs to be on of {periods}"

        # to date provided but from date wasn't provided
        if to_date and not from_date:
            raise DateRangeError("To date provided without a from date")

        if from_date and to_date:
            # compare dates:
            if pd.to_datetime(to_date) < pd.to_datetime(from_date):
                raise DateRangeError("To date needs to be after from date")
            url = f"{self.base_path}/{EndPoint.EOD.value}/{symbol_code}.{exchange_code}?api_token={self.api_token}&order={order}&period={period}&from={from_date}&to={to_date}&fmt=json"
        elif from_date:
            # no to_date, will default to today
            logger.info(f"Querrying eod for {symbol_code} from {from_date}")
            url = f"{self.base_path}/{EndPoint.EOD.value}/{symbol_code}.{exchange_code}?api_token={self.api_token}&order={order}&period={period}&from={from_date}&fmt=json"

        else:
            url = f"{self.base_path}/{EndPoint.EOD.value}/{symbol_code}.{exchange_code}?api_token={self.api_token}&order={order}&period={period}&fmt=json"

        response = self._query(url)

        df_data = pd.DataFrame(response)

        return df_data

    def stock_fundamentals(
        self, exchange_code: str, symbol_code: str
    ) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        """
        Get fundamental data for BOND given id
        :param exchange_code: code of the exchange
        :param symbol_code: code of the asset
        """
        url = f"{self.base_path}/{EndPoint.FUNDAMENTALS.value}/{symbol_code}.{exchange_code}?api_token={self.api_token}&fmt=json"

        response = self._query(url)

        return response

    def get_macro(
        self, country: str, indicator: str, order: str = "a", period: str = "q"
    ) -> pd.DataFrame:

        url = f"{self.base_path}/{EndPoint.MACRO.value}/{country}?indicator={indicator}&api_token={self.api_token}&order={order}&period={period}&fmt=json"

        response = self._query(url)

        df_data = pd.DataFrame(response)

        return df_data

    def bond_data(self, ISIN: str, from_date: str, to_date: str) -> pd.DataFrame:
        """
        Get end of day data for specific bond for date range

        :param ISIN: bond identifer
        :param from_date: start date
        :param to_date: end date
        """
        return self.eod_data("BOND", ISIN, from_date, to_date)

    def bond_fundamentals(
        self, id: str
    ) -> Union[Dict[Any, Any], List[Dict[str, str]], None]:
        """
        Get fundamental data for BOND given id
        :param id: can be either CUSIP or ISIN (USA)
        """
        url = f"{self.base_path}/{EndPoint.BOND_FUNDAMENTALS}/{id}?api_token={self.api_token}"

        response = self._query(url)

        return response
