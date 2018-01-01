"""Tests for HTTP_client.py"""
from unittest.mock import MagicMock

import pytest
import requests
from collections import OrderedDict

from StockScraper.Generic.exceptions import HTTPError
from StockScraper.Clients.http_client import validate_response, JSONClient
from StockScraper.Clients.http_client import HTTPClient


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
    with pytest.raises(TypeError) as excinfo:
        client.call_endpoint('TEST', 'test')
    excinfo.match('Method TEST does not match REST API METHODS:')


def test_create_endpoint_url(mocker):
    client = HTTPClient('http://localhost')
    settings = OrderedDict()
    settings['value1'] = 1
    settings['value2'] = 2
    url_string = client.create_endpoint_url(url_root='test_url_root/base', settings=settings)
    assert url_string == 'test_url_root/base?value1=1&value2=2'


def test_repr():
    client = HTTPClient('http://localhost')
    assert client.__repr__() == 'HTTPClient - http://localhost'


def test_to_json_mixin(mocker):
    json_client = JSONClient()
    mocked = MagicMock()
    mocked.content = '{"hello": "world"}'
    assert isinstance(json_client.to_json(mocked), dict)
