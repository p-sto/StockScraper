"""Tests for BankierClient class"""

from unittest.mock import MagicMock

from StockScraper.Clients.BankierClient.bankier_client import BankierClient


def test_bankier_client(mocker):
    client = BankierClient()
    mocked = MagicMock()
    mocked.status_code = 200
    mocked.url = 'http://localhost'
    mocked.content = '{"hello": "world"}'
    mocked_get = mocker.patch('requests.get')
    mocked_get.return_value = mocked
    returned = client.get_market_data(company_symbol='test', days_back=10)
    assert returned == {'hello': 'world'}
