StockSraper
===========

Scrapper for Bankier.pl.

Preparation
-----------

::
    $ git clone

    $ cd StockScraper

    $ make venv

    $ source venv/bin/activate

    $ export PYTHONPATH=$path_to_project


Usage
-----

.. code:: python

    from StockScraper.Generic.Configuration import get_data_from_config
    from StockScraper.Generic.Clients import get_client

    client = get_client("http://www.bankier.pl")
    data = client.get_data(symbol="OPONEO.PL", days=10)
    print(data)

Example can be found in StockScraper/demo.py
