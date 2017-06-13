"""Tests for Clients.py"""

import pytest

from StockScraper.Generic.Clients import get_client
from StockScraper.Clients.Bankier_client import BankierClient


def test_get_clients():
    assert isinstance(get_client('http://www.bankier.pl'), BankierClient)
    with pytest.raises(NotImplementedError):
        get_client('test')