"""File contains definition of HTTP clients """
from datetime import datetime
from urllib.parse import urljoin
import logging
import requests

from StockScraper.Generic.exceptions import HTTPError


REST_API_METHODS = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']


def validate_response(called_method):
    """Decorator for HTTPClient validating received response for REST API methods.
    If status code from server is different than 200 raises HTTPError.

    :param called_method: requests methods - POST, GET, PUT, PATH, DELETE
    :return: response from server
    """
    def wrapper(method, endpoint, *args, **kwargs):
        """Executes decorated function and checks status_code."""
        resp = called_method(method, endpoint, *args, **kwargs)
        if resp.status_code != 200:
            logging.error('HTTP Client returned status code %s for url %s', resp.status_code, resp.url)
            raise HTTPError('HTTP Client returned status code {0} for url {1}'.format(str(resp.status_code), resp.url))
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
        logging.info('Calling method %s for endpoint %s', method, endpoint)

        if method.upper() not in REST_API_METHODS:
            logging.error('Method %s does not match REST API METHODS: %s', method, ','.join(REST_API_METHODS))
            raise TypeError('Method {0} does not match REST API METHODS: {1}'.format(str(method),
                                                                                     ','.join(REST_API_METHODS)))

        req_method = getattr(requests, method.lower())
        resp = req_method(urljoin(self.host_name, endpoint), *args, **kwargs)
        return resp

    @staticmethod
    def create_endpoint_url(symbol: str, date_from: datetime = None, date_to: datetime = None, days: int = None):
        """Abstract method for creating endpoint url."""
        raise NotImplementedError


class JSONClient:   # pylint: disable=too-few-public-methods
    """Mixin for JSON client."""
    @staticmethod
    def to_json(response):
        """Convert response from requests to json object.

        :param response: response from requests
        :return: json object
        """
        return response.json()
