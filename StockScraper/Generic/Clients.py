"""Generic mechanisms to deal with clients."""

import logging

from StockScraper.Clients.Bankier_client import BankierClient


def get_client(client_type):
    """Return json configuration file.

    :param client_type: name of a client
    :return: Client instance
    """
    logging.info('Creating client for type {0}'.format(client_type))
    if client_type == 'http://www.bankier.pl':
        return BankierClient()

    err = 'Client not defined for client type: {0}'.format(client_type)
    logging.error(err)
    raise NotImplementedError(err)
