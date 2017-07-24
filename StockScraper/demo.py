"""Main script file"""

import os
import logging

from pathlib import Path
from StockScraper.Generic.configuration import get_data_from_config
from StockScraper.Generic.clients import get_client


def main() -> None:
    """Presentation of created scrapper.

    :return: None
    """
    logging.basicConfig(filename='StockScraper.log')

    path_to_config = Path(os.path.dirname(os.path.abspath(__file__)))
    path_to_config = path_to_config / 'Configs' / 'config.json'
    config = get_data_from_config(str(path_to_config))

    for host in config:
        print('Loading data for host {}'.format(host))
        client = get_client(host)
        for company in config[host]:
            print('Working on {}'.format(company))
            data = client.get_data(symbol=company, days=10)
            print(data)

if __name__ == '__main__':
    main()
