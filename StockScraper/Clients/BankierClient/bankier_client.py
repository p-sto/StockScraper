""" Contains implementation of Bankier.pl client."""

from datetime import timedelta, datetime

from typing import Optional
from StockScraper.Generic.timeoperations import TimeOperate
from StockScraper.Clients.http_client import HTTPClient
from StockScraper.Clients.http_client import JSONClient


class BankierClient(JSONClient, HTTPClient):    # type: ignore
    """Bankier.pl client."""

    def __init__(self, host_name: str = 'http://www.bankier.pl') -> None:   # pylint: disable=useless-super-delegation
        super(BankierClient, self).__init__(host_name)

    def get_market_data(self, company_symbol: str,
                        days_back: int = 7,
                        date_to: datetime = TimeOperate.get_current_time_utc(),
                        date_from: Optional[datetime] = None) -> dict:
        """Return data for Bankier.pl for specific symbol and date range.

        :param company_symbol: name of a company for which data should be downloaded
        :param date_from: datetime object
        :param date_to: datetime object
        :param days_back: how many days before date_from data should be collected
        :return: data from service
        """
        if not date_from:
            assert isinstance(date_to, datetime)
            date_from = date_to - timedelta(days=float(days_back))

        utc_date_to = TimeOperate.to_utc(date_to)
        utc_date_from = TimeOperate.to_utc(date_from)
        epoch_date_to = TimeOperate.days_in_epoch(utc_date_to)
        epoch_date_from = TimeOperate.days_in_epoch(utc_date_from)

        settings = {'symbol': company_symbol,
                    'today': 'false',
                    'intraday': 'false',
                    'type': 'area',
                    'init': 'false',
                    'date_from': str(epoch_date_from),
                    'date_to': str(epoch_date_to)}
        url_root = 'new-charts/get-data'
        endpoint_url = self.create_endpoint_url(url_root, settings)
        return self.to_json(self.call_endpoint('get', endpoint_url))
