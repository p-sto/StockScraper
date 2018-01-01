"""Main script file"""
import os
import configparser
import logging

from pathlib import Path

from StockScraper.Clients.BankierClient.bankier_client import BankierClient
from StockScraper.Generic.configuration import get_data_from_config
from StockScraper.Generic.clients import get_client

try:
    SCRAPER_HOME = os.environ['SCRAPER_HOME']
    logging.info('SCRAPER_HOME =  %s', SCRAPER_HOME)
except KeyError:
    err = 'Environment variable SCRAPER_HOME not set'
    raise KeyError(err)


def main() -> None:
    """Presentation of created scrapper.

    :return: None
    """
    logging.basicConfig(filename='StockScraper.log')

    config_parser = configparser.ConfigParser()
    config_parser.read(SCRAPER_HOME + '/project.cfg')

    path_to_config = Path(config_parser['DEFAULT']['configs_path']) / 'config.json'
    client_config = get_data_from_config(str(path_to_config))

    for host in client_config:
        logging.info('Loading data for host {}'.format(host))
        client = get_client(host)
        if isinstance(client, BankierClient):
            for company_symbol in client_config[host]:
                logging.info('Getting data for {}'.format(company_symbol))
                data = client.get_market_data(company_symbol=company_symbol, days_back=10)


if __name__ == '__main__':
    main()
