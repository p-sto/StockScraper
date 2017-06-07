"""Generic mechanisms to deal with clients."""

from StockScraper.Clients.Bankier_client import BankierClient


def get_client(client_type):
    """Return json configuration file.

    :param client_type: path to configuration file
    :return: Client instance
    """
    if client_type == 'http://www.bankier.pl':
        return BankierClient()

    raise NotImplemented('Client not defined for client type: {0}'.format(client_type))
