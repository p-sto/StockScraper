StockScraper
============

Scraper for Bankier.pl.

Preparation
-----------

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
    data = client.get_data(symbol="OPONEO.PL", days=10)
    print(data)

Example can be found in demo.py
