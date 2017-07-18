"""Tests for Clients.py"""

import pytest

from StockScraper.Generic.clients import get_client
from StockScraper.Clients.bankier_client import BankierClient


def test_get_clients():
    assert isinstance(get_client('http://www.bankier.pl'), BankierClient)
    with pytest.raises(NotImplementedError) as excinfo:
        get_client('test')
    excinfo.match('Client not defined for client type: test')
