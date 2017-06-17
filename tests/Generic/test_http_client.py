"""Tests for HTTP_client.py"""

import pytest
import requests

from StockScraper.Generic.Exceptions import HTTPError
from StockScraper.Generic.HTTP_client import validate_response
from StockScraper.Generic.HTTP_client import HTTPClient


def test_validate_response(mocker):
    mocked = mocker.patch('requests.get')
    mocked.return_value.status_code = 200
    mocked.return_value.url = 'http://localhost'

    @validate_response
    def testing_get(method, endpoint):
        req_method = getattr(requests, method.lower())
        resp = req_method(endpoint)
        return resp

    assert testing_get('GET', 'http://localhost').status_code == 200

    mocked.return_value.status_code = 201
    with pytest.raises(HTTPError):
        testing_get('GET', 'http://localhost')


def test_http_client(mocker):
    mocked = mocker.patch('requests.get')
    mocked.return_value.status_code = 200
    mocked.return_value.url = 'http://localhost'
    client = HTTPClient('http://localhost')
    assert client.call_endpoint('GET', 'test').status_code == 200
    with pytest.raises(TypeError):
        client.call_endpoint('TEST', 'test')
