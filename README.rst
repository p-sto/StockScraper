.. image:: https://travis-ci.org/stovorov/StockScraper.svg?branch=master
    :target: https://travis-ci.org/stovorov/StockScraper

.. image:: https://codecov.io/gh/stovorov/StockScraper/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/stovorov/StockScraper

StockScraper
============

Repo contains scrapper for ``Bankier.py`` service which delivers online information about current stocks exchange prices on
GPW - Polish stock exchange.


Getting Started
---------------

::

    $ git clone
    $ cd StockScraper
    $ make venv
    $ source venv/bin/activate
    $ source prepare.sh


Usage
-----

.. code:: python

    from StockScraper.Generic.Clients import get_client

    client = get_client("http://www.bankier.pl")
    data = client.get_market_data(company_symbol="OPONEO.PL", days_back=10)
    print(data)

Example can be found in demo.py
