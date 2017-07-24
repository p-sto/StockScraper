"""Generic mechanisms to deal with clients."""

import logging

from StockScraper.Clients.bankier_client import BankierClient
from StockScraper.Generic.http_client import HTTPClient


def get_client(client_type: str) -> HTTPClient:
    """Return json configuration file.

    :param client_type: name of a client
    :return: Client instance
    """
    logging.info('Creating client for type %s', client_type)
    if client_type == 'http://www.bankier.pl':
        return BankierClient()

    logging.error('Client not defined for client type: %s', client_type)
    raise NotImplementedError('Client not defined for client type: {0}'.format(client_type))
