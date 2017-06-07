"""File contains definition of HTTP clients """

import requests

from urllib.parse import urljoin
from StockScraper.Generic.Exceptions import HTTPError


REST_API_METHODS = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']


def validate_response(called_method):
    """Decorator for HTTPClient validating received response for REST API methods.
    If status code from server is different than 200 raises HTTPError.

    :param called_method: requests methods - POST, GET, PUT, PATH, DELETE
    :return: response from server
    """
    def wrapper(method, endpoint, *args, **kwargs):
        resp = called_method(method, endpoint, *args, **kwargs)
        if resp.status_code != 200:
            err = 'HTTP Client returned status code {0} for url {1}'.format(str(resp.status_code), resp.url)
            raise HTTPError(err)
        return resp
    return wrapper


class HTTPClient:
    """Definition of HTTP client. """

    def __init__(self, host_name):
        """Initialize object.

        :param host_name: string containing host name
        :return: None
        """
        self.host_name = host_name

    @validate_response
    def call_endpoint(self, method, endpoint, *args, **kwargs):
        """Call api endpoint method.

        :param method: REST API methods name (string) - 'POST', 'GET', 'PUT', 'PATCH', 'DELETE'
        :param endpoint: endpoint which will be called with method.
        :param args: additional arguments
        :param kwargs: additional key-worded arguments
        :return:
        """
        if method.upper() not in REST_API_METHODS:
            err = 'Method {0} does not match REST API METHODS: {1}'.format(str(method), ','.join(REST_API_METHODS))
            raise TypeError(err)
        req_method = getattr(requests, method.lower())
        resp = req_method(urljoin(self.host_name, endpoint), *args, **kwargs)
        return resp

    @staticmethod
    def generate_endpoint(**kwargs):
        raise NotImplementedError


class JSONClient:
    """Mixin for JSON client."""
    @staticmethod
    def to_json(response):
        """Convert response from requests to json object.

        :param response: response from requests
        :return: json object
        """
        return response.json()
