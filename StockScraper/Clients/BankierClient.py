""" Contains implementation of Bankier.pl client."""

from collections import OrderedDict
from datetime import timedelta

from StockScraper.Generic.Datetime import Date
from StockScraper.Generic.HTTP_client import HTTPClient
from StockScraper.Generic.HTTP_client import JSONClient


class BankierClient(JSONClient, HTTPClient):
    """Bankier.pl client."""

    def __init__(self, host_name='http://www.bankier.pl'):
        super(BankierClient, self).__init__(host_name)

    def call_endpoint(self, method, endpoint, *args, **kwargs):
        """Call method on specific endpoint.

        :param method: operation to be performed e.g. GET
        :param endpoint: url to endpoint
        :param args: additional positional arguments
        :param kwargs: additional key-worded arguments
        :return: response from endpoint in json format
        """
        resp = super(BankierClient, self).call_endpoint(method, endpoint, *args, **kwargs)
        return self.to_json(resp)

    @staticmethod
    def create_endpoint_url(symbol=None, date_from=None, date_to=None, days=None):
        """Create endpoint url to data from Bankier.pl.
        :param symbol: Name of symbol - name of a company
        :param date_from: datetime object
        :param date_to: datetime object
        :return: url to the endpoint
        """
        if not days:
            days = 3

        if not date_to:
            date_to = Date.get_current_time_utc()

        if not date_from:
            date_from = date_to - timedelta(days=days)

        utc_date_to = Date.to_utc(date_to)
        utc_date_from = Date.to_utc(date_from)

        epoch_date_to = Date.days_in_epoch(utc_date_to)
        epoch_date_from = Date.days_in_epoch(utc_date_from)
        # TODO: there are some problems with weekends...
        settings = [('today', 'false'), ('intraday', 'false'),
                    ('type', 'area'), ('init', 'false'),
                    ('date_from', str(epoch_date_from)), ('date_to', str(epoch_date_to))]

        settings = OrderedDict(settings)

        endpoint_url = 'new-charts/get-data?symbol=' + symbol + '&'
        endpoint_url += '&'.join([x + '=' + settings[x] for x in settings])
        return endpoint_url

    def get_data(self, symbol, date_from=None, date_to=None, days=3):
        """Return data for Bankier.pl for specific symbol and date range.

        :param symbol: name of a company for which data should be downloaded
        :param date_from: datetime object
        :param date_to: datetime object
        :param days: how many days before date_from data should be collected
        :return: data from service
        """
        endpoint_url = self.create_endpoint_url(symbol, date_from, date_to, days)
        return self.call_endpoint('get', endpoint_url)
